<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Contable extends Model
{
    protected $fillable = [
        'id_documento',
        'id_comprobante',
        'id_nit',
        'fecha',
        'fecha_manual',
        'id_cuenta',
        'valor',
        'tipo',
        'concepto',
        'documento_referencia',
        'token',
        'extra',
    ];
}
