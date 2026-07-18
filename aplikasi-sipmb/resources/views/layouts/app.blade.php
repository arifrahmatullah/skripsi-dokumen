<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">

        <title>{{ config('app.name') }}</title>

        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,500,600,700&display=swap" rel="stylesheet" />

        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="font-sans antialiased bg-gray-50 text-gray-800">
        <div class="h-screen flex overflow-hidden">
            {{-- Sidebar --}}
            <aside class="w-60 shrink-0 bg-brand-950 text-white flex flex-col">
                <div class="h-16 flex items-center gap-2.5 px-6 border-b border-white/10">
                    <span class="w-8 h-8 rounded-lg bg-accent-500 flex items-center justify-center font-bold text-sm">P</span>
                    <span class="font-bold tracking-tight leading-none">SI-PMB<br><span class="text-[11px] font-normal text-brand-200">Tazkia</span></span>
                </div>

                @php
                    $menu = [
                        ['route' => 'dashboard', 'label' => 'Dashboard'],
                        ['route' => 'crispdm.index', 'label' => 'Proses CRISP-DM'],
                        ['route' => 'pendaftar.index', 'label' => 'Data Pendaftar'],
                        ['route' => 'prediksi.index', 'label' => 'Prediksi Data Baru'],
                        ['route' => 'klasifikasi.index', 'label' => 'Hasil Klasifikasi'],
                        ['route' => 'rekomendasi.index', 'label' => 'Rekomendasi'],
                        ['route' => 'laporan.index', 'label' => 'Laporan'],
                    ];
                @endphp
                <nav class="flex-1 py-4 space-y-0.5 px-3 overflow-y-auto">
                    @foreach ($menu as $item)
                        @php $active = request()->routeIs($item['route'].'*'); @endphp
                        <a href="{{ route($item['route']) }}"
                           class="flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm transition {{ $active
                                ? 'bg-white/10 text-white font-semibold'
                                : 'text-brand-200 hover:bg-white/5 hover:text-white' }}">
                            <span class="w-1.5 h-1.5 rounded-full {{ $active ? 'bg-accent-500' : 'bg-brand-400' }}"></span>
                            {{ $item['label'] }}
                        </a>
                    @endforeach
                </nav>

                <div class="p-3 border-t border-white/10">
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button type="submit" class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm text-brand-200 hover:bg-white/5 hover:text-white transition">
                            <span class="w-1.5 h-1.5 rounded-full bg-brand-400"></span>
                            Logout
                        </button>
                    </form>
                </div>
            </aside>

            <div class="flex-1 min-w-0 flex flex-col">
                {{-- Header --}}
                <header class="h-16 shrink-0 bg-white border-b border-gray-100 flex items-center justify-between px-8">
                    @isset($header)
                        <div>{{ $header }}</div>
                    @else
                        <div></div>
                    @endisset

                    <x-dropdown align="right" width="48">
                        <x-slot name="trigger">
                            <button class="flex items-center gap-2.5 text-sm text-gray-600 hover:text-gray-900">
                                <span class="w-9 h-9 rounded-full bg-accent-500 flex items-center justify-center text-white text-sm font-bold">
                                    {{ strtoupper(substr(auth()->user()->name, 0, 1)) }}
                                </span>
                                <span class="font-medium">{{ auth()->user()->name }}</span>
                            </button>
                        </x-slot>
                        <x-slot name="content">
                            <x-dropdown-link :href="route('profile.edit')">{{ __('Profil') }}</x-dropdown-link>
                            <form method="POST" action="{{ route('logout') }}">
                                @csrf
                                <x-dropdown-link :href="route('logout')"
                                        onclick="event.preventDefault(); this.closest('form').submit();">
                                    {{ __('Log Out') }}
                                </x-dropdown-link>
                            </form>
                        </x-slot>
                    </x-dropdown>
                </header>

                {{-- Main content --}}
                <main class="flex-1 min-w-0 p-8 overflow-y-auto">
                    @if (session('status'))
                        <div class="mb-5 px-4 py-3 rounded-lg bg-brand-50 border border-brand-200 text-brand-800 text-sm font-medium">
                            {{ session('status') }}
                        </div>
                    @endif

                    {{ $slot }}
                </main>
            </div>
        </div>
    </body>
</html>
