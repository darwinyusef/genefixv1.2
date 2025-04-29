<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class CausacionContable extends Model
{
    protected $table = 'causacioncontable';
    use HasFactory;

    protected $primaryKey = 'id_documento';

    protected $fillable = [
        'id',
        'user_id',
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
        'estado'
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
