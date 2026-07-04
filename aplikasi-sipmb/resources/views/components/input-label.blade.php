@props(['value'])

<label {{ $attributes->merge(['class' => 'block font-semibold text-xs uppercase tracking-wide text-gray-500']) }}>
    {{ $value ?? $slot }}
</label>
