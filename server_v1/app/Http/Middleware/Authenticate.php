<?php

namespace App\Http\Middleware;

use Closure;
use Exception;
use Tymon\JWTAuth\Facades\JWTAuth;

class Authenticate
{
    public function handle($request, Closure $next)
    {
        try {
            $user = JWTAuth::parseToken()->authenticate();
            if (!$user) {
                return response()->json(['error' => 'Usuario no autenticado'], 401);
            }
        } catch (Exception $e) {
            return response()->json(['error' => 'Token inválido o no enviado', 'detalle' => $e->getMessage()], 401);
        }

        return $next($request);
    }
}