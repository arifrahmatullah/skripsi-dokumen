<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">

        <title>{{ config('app.name', 'Laravel') }}</title>

        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,500,600,700&display=swap" rel="stylesheet" />

        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="font-sans antialiased">
        <div class="min-h-screen flex items-center justify-center bg-brand-950 relative overflow-hidden px-4">
            <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-accent-500/20 blur-3xl"></div>
            <div class="absolute -bottom-32 -left-24 w-96 h-96 rounded-full bg-brand-500/30 blur-3xl"></div>

            <div class="relative w-full sm:max-w-md">
                <div class="text-center mb-6">
                    <div class="mx-auto w-14 h-14 rounded-2xl bg-accent-500 flex items-center justify-center font-bold text-white text-lg shadow-lg shadow-accent-900/30">
                        P
                    </div>
                    <h1 class="mt-4 text-xl font-bold text-white">SI-PMB Tazkia</h1>
                    <p class="text-sm text-brand-200">Rekomendasi Tindak Lanjut Konfirmasi Pendaftaran</p>
                </div>

                <div class="w-full px-8 py-8 bg-white shadow-xl rounded-2xl">
                    {{ $slot }}
                </div>
            </div>
        </div>
    </body>
</html>
