<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\CausacionContable;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Storage;
use Illuminate\Filesystem\FilesystemAdapter;
use Carbon\Carbon;

class CausacionContableController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request)
    {
        $perPage = $request->input('per_page', 10); // cantidad por página
        $page = $request->input('page', 1);
        $offset = ($page - 1) * $perPage;
        $sortDirection = $request->input('order', 'desc');
        $sortField = $request->input('sort', 'created_at');
        $data = CausacionContable::where('user_id', Auth::id())
            ->where('estado', 'abierto')
            ->orderBy($sortField, $sortDirection)
            ->skip($offset)
            ->take($perPage)
            ->get();

        $total = CausacionContable::where('user_id', Auth::id())->where('estado', 'abierto')->count();

        return response()->json([
            'data' => $data,
            'total' => $total,
            'current_page' => $page,
            'per_page' => $perPage,
            'last_page' => ceil($total / $perPage),
        ]);
    }

    public function sendingFile(Request $request)
    {
        $request->validate([
            'archivo' => 'required|file|max:10240' // máx 10MB
        ]);
        // Capturamos el archivo
        $archivo = $request->file('archivo');

        // Subimos el archivo a la carpeta 'enero/' en S3 y generamos nombre único
        // $ruta = $archivo->store('enero', 's3');
        $mesNumero = Carbon::now()->month;
        $ruta = Storage::disk('s3')->putFile($mesNumero, $archivo);
        // $url = Storage::disk('s3')->put('enero/', $ruta);
        dd($ruta);
        return response()->json(['url' => $ruta]);
    }

    public function getRoute(Request $request)
    {
        /** @var FilesystemAdapter $disk */
        $disk = Storage::disk('s3');

        $url = $disk->temporaryUrl($request->url, now()->addMinutes(10));
        dd($url);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'id_comprobante' => 'required|integer',
            'id_nit' => 'required|integer',
            'fecha' => 'required|date',
            'fecha_manual' => 'required|date',
            'id_cuenta' => 'required|integer',
            'valor' => 'required|numeric',
            'tipo' => 'required|integer',
            'concepto' => 'required|string',
            'documento_referencia' => 'nullable|string',
            'token' => 'nullable|string',
            'extra' => 'nullable|string',
        ]);

        $data['user_id'] = Auth::id();

        return CausacionContable::create($data);
    }

    public function show($id)
    {
        $documento = CausacionContable::where('id', $id)->where('user_id', Auth::id())->firstOrFail();
        return response()->json($documento);
    }

    public function update(Request $request, $id)
    {
        $documento = CausacionContable::where('id', $id)->where('user_id', Auth::id())->firstOrFail();

        $data = $request->validate([
            'id_comprobante' => 'sometimes|integer',
            'id_nit' => 'sometimes|integer',
            'fecha' => 'sometimes|date',
            'fecha_manual' => 'sometimes|date',
            'id_cuenta' => 'sometimes|integer',
            'valor' => 'sometimes|numeric',
            'tipo' => 'sometimes|integer',
            'concepto' => 'sometimes|string',
            'documento_referencia' => 'nullable|string',
            'token' => 'nullable|string',
            'extra' => 'nullable|string',
        ]);

        $documento->update($data);

        return $documento;
    }

    public function destroy($id)
    {
        $documento = CausacionContable::where('id_documento', $id)->where('user_id', Auth::id())->firstOrFail();
        $documento->delete();
        return response()->json(['message' => 'Documento eliminado']);
    }
}
