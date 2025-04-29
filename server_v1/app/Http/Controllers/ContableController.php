<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Contable;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Http;

class ContableController extends Controller
{
    public function nitFilter(Request $request)
    {
        // Validar los datos entrantes
        $validator = Validator::make($request->all(), [
            'nit' => 'required|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => $validator->errors()], 400);
        }

        // Obtener el NIT del cuerpo de la solicitud
        $nit = $request->input('nit');

        // Realizar la consulta a la API externa
        //http://begranda.com/equilibrium2/public/api/nits?key=${API_KEY}&f-nit_1=123&eq-nit_1=${valor}
        $response = Http::get('http://begranda.com/equilibrium2/public/api/nits', [
            'key' => env('BEGRANDA_EAPI_KEY'),
            'f-nit_1=123' => '123',
            'eq-nit_1' => $nit,
        ]);

        // Verificar la respuesta de la API externa
        if ($response->failed()) {
            return response()->json(['error' => 'Error al obtener el NIT de la API externa'], $response->status());
        }

        // Devolver la respuesta de la API externa
        return response()->json($response->json());
    }

    
    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */

    public function enviarDocumentos(Request $request)
    {
        // Validar los datos entrantes
        $validator = Validator::make($request->all(), [
            'documents' => 'required|json',
            'bearer_token' => 'required|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => $validator->errors()], 400);
        }

        // Obtener los documentos y el token del cuerpo de la solicitud
        $documents = json_decode($request->input('documents'), true);
        $bearerToken = $request->input('bearer_token');

        // Enviar los datos a la API externa
        // $response = Http::withHeaders([
        //     'Authorization' => 'Bearer ' . $bearerToken,
        // ])->attach(
        //     'documents',
        //     json_encode($documents)
        // )->post('http://begranda.com/equilibrium2/public/api/document', [
        //     'key' => env('API_KEY'),
        // ]);

        // Verificar la respuesta de la API externa
        // if ($response->failed()) {
        //     return response()->json(['error' => 'Error al enviar los documentos a la API externa'], $response->status());
        // }


        // Almacenar los documentos en la base de datos
        foreach ($documents as $doc) {
            Contable::create($doc);
        }

        return response()->json(['message' => 'Documentos enviados y almacenados exitosamente']);
    }
}
