@props(['disabled' => false])

<input @disabled($disabled) {{ $attributes->merge(['class' => 'border-gray-200 bg-gray-50 text-gray-800 focus:border-brand-500 focus:bg-white focus:ring-brand-500 rounded-lg shadow-sm text-sm transition']) }}>
