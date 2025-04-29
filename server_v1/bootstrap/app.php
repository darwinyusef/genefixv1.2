<?php



require_once __DIR__ . '/../vendor/autoload.php';

(new Laravel\Lumen\Bootstrap\LoadEnvironmentVariables(
    dirname(__DIR__)
))->bootstrap();

date_default_timezone_set(env('APP_TIMEZONE', 'UTC'));

/*
|--------------------------------------------------------------------------
| Create The Application
|--------------------------------------------------------------------------
|
| Here we will load the environment and create the application instance
| that serves as the central piece of this framework. We'll use this
| application as an "IoC" container and router for this framework.
|
*/

$app = new Laravel\Lumen\Application(
    dirname(__DIR__)
);



// Cargar la configuración de vistas y habilitar Blade
$app->singleton('view', function ($app) {
    // Definir la ruta donde están tus vistas Blade
    $viewPath = base_path('resources/views');
    
    // Crear un sistema de archivos
    $fileSystem = new Filesystem();

    // Cargar las vistas con Blade
    $viewFinder = new FileViewFinder($fileSystem, [$viewPath]);
    $cache = storage_path('framework/views'); // Ruta donde se almacenarán las vistas compiladas
    $compiler = new BladeCompiler($fileSystem, $cache);

    // Crear un EngineResolver y registrar el CompilerEngine
    $engineResolver = new Illuminate\View\Engines\EngineResolver();
    $engineResolver->register('blade', function () use ($compiler) {
        return new CompilerEngine($compiler);
    });

    // Fábrica de vistas
    $viewFactory = new Factory($engineResolver, $viewFinder, $app['events']);
    
    return $viewFactory;
});

$app->withFacades();

$app->withEloquent();

/*
|--------------------------------------------------------------------------
| Register Container Bindings
|--------------------------------------------------------------------------
|
| Now we will register a few bindings in the service container. We will
| register the exception handler and the console kernel. You may add
| your own bindings here if you like or you can make another file.
|
*/

$app->singleton(
    Illuminate\Contracts\Debug\ExceptionHandler::class,
    App\Exceptions\Handler::class
);

$app->singleton(
    Illuminate\Contracts\Console\Kernel::class,
    App\Console\Kernel::class
);

/*
|--------------------------------------------------------------------------
| Register Config Files
|--------------------------------------------------------------------------
|
| Now we will register the "app" configuration file. If the file exists in
| your configuration directory it will be loaded; otherwise, we'll load
| the default version. You may register other files below as needed.
|
*/

// $app->configure('app');
$app->configure('auth');

/*
|--------------------------------------------------------------------------
| Register Middleware
|--------------------------------------------------------------------------
|
| Next, we will register the middleware with the application. These can
| be global middleware that run before and after each request into a
| route or middleware that'll be assigned to some specific routes.
|
*/

$app->middleware([
    \App\Http\Middleware\CorsMiddleware::class,
]);

$app->routeMiddleware([
    'auth' => App\Http\Middleware\Authenticate::class,
]);

// También esto si no lo tenés
class_alias(Tymon\JWTAuth\Facades\JWTAuth::class, 'JWTAuth');
class_alias(Tymon\JWTAuth\Facades\JWTFactory::class, 'JWTFactory');

/*
|--------------------------------------------------------------------------
| Register Service Providers
|--------------------------------------------------------------------------
|
| Here we will register all of the application's service providers which
| are used to bind services into the container. Service providers are
| totally optional, so you are not required to uncomment this line.
|
*/

// $app->register(App\Providers\AppServiceProvider::class);
// $app->register(App\Providers\AuthServiceProvider::class);
// $app->register(App\Providers\EventServiceProvider::class);

$app->register(Tymon\JWTAuth\Providers\LumenServiceProvider::class);

/*
|--------------------------------------------------------------------------
| Load The Application Routes
|--------------------------------------------------------------------------
|
| Next we will include the routes file so that they can all be added to
| the application. This will provide all of the URLs the application
| can respond to, as well as the controllers that may handle them.
|
*/

$app->router->group([
    'namespace' => 'App\Http\Controllers',
], function ($router) {
    require __DIR__ . '/../routes/web.php';
});

// Registrar el middleware CORS de forma global
$app->middleware([
    \Illuminate\Http\Middleware\HandleCors::class
]);

$app->routeMiddleware([
    'auth' => App\Http\Middleware\Authenticate::class,
]);

return $app;
