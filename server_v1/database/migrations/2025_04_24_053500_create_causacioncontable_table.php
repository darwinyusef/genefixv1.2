<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('causacioncontable', function (Blueprint $table) {
            $table->id();
            $table->integer('id_documento')->nullable();
            $table->unsignedBigInteger('id_comprobante');
            $table->unsignedBigInteger('id_nit');
            $table->dateTime('fecha');
            $table->date('fecha_manual');
            $table->unsignedBigInteger('id_cuenta');
            $table->decimal('valor', 15, 2);
            $table->tinyInteger('tipo');
            $table->text('concepto');
            $table->string('documento_referencia')->nullable();
            $table->string('token')->nullable();
            $table->text('extra')->nullable();
            $table->unsignedBigInteger('user_id');
            $table->string('estado')->default('entregado');
            $table->timestamps();

            $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('causacioncontable');
    }
};
