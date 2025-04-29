<?php

/** @var \Laravel\Lumen\Routing\Router $router */

use App\Http\Controllers\AuthController;
use App\Http\Controllers\CausacionContableController;
use App\Http\Controllers\ContableController;
use App\Http\Controllers\PasswordResetController;

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/', function () use ($router) {
    return response()->json([
        "error" => "Bienvenido a nuestra API GeneFIX",
        "authorization" => "Usted no tiene permisos",
        "code" => 404
    ], 404);
});

$router->post('/check-document', ['uses' => 'AuthController@checkDocument']);
$router->post('/active-user', ['uses' => 'AuthController@activeUser']);
$router->post('/login', ['uses' => 'AuthController@login']);
$router->post('/register', ['uses' => 'AuthController@register']);
$router->get('/register-service', ['uses' => 'AuthController@serviceRegister']);

$router->post('/password/email', ['uses' => 'PasswordResetController@sendResetLinkEmail']);
$router->post('/password/reset', ['uses' => 'PasswordResetController@resetPassword']);
$router->post('/forgot-username', ['uses' => 'PasswordResetController@forgotUsername']);

// $router->post('/causacion-contable', ['uses' => 'ContableController@store']); // ← Comentada (era con Passport)

$router->post('/subir', ['uses' => 'CausacionContableController@sendingFile', 'as' => 'sending.archivo']);
$router->get('/fileroute', ['uses' => 'CausacionContableController@getRoute', 'as' => 'get.route']);
$router->get('/nit', ['uses' => 'ContableController@nitFilter', 'as' => 'get.nit.filter']);


$router->group(['middleware' => 'auth'], function () use ($router) {
    $router->get('/user', ['uses' => 'AuthController@user']);
    $router->post('/logout', ['uses' => 'AuthController@logout']);

    // CRUD manual para causacion-contable
    $router->get('/causacion-contable', ['uses' => 'CausacionContableController@index']);
    $router->post('/causacion-contable', ['uses' => 'CausacionContableController@store']);
    $router->get('/causacion-contable/{id}', ['uses' => 'CausacionContableController@show']);
    $router->put('/causacion-contable/{id}', ['uses' => 'CausacionContableController@update']);
    $router->delete('/causacion-contable/{id}', ['uses' => 'CausacionContableController@destroy']);
});
