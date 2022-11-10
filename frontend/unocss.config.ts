import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetTypography,
  presetUno,
  presetWebFonts,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss'

export default defineConfig({
  shortcuts: [
    ['btn', 'px-2 border-2 font-light border-rounded-10px opacity-75 text-truegray transition duration-200 ease-in-out dark:hover:text-white cursor-pointer hover:bg-sky-400 dark:hover:border-white hover:border-dark hover:text-dark disabled:cursor-default disabled:bg-neutral-300 disabled:dark:bg-dark-100 disabled:opacity-50'],
    ['icon-btn', 'inline-block cursor-pointer select-none opacity-75 transition duration-200 ease-in-out hover:opacity-100 hover:text-sky-400'],
    ['text-field', 'flex h-36px w-250px items-center bg-neutral-200 dark:bg-dark8 px-3 rounded-10px opacity-75 text-gray-700 dark:text-gray-200 dark:hover:bg-dark hover:bg-neutral300 outline-none'],
    ['animation', 'transition duration-200 ease-in-out'],
    ['title1', 'text-30px lg:text-40px font-bold opacity-75 text-gray-700 dark:text-gray-200'],
    ['title2', 'text-25px lg:text-30px font-bold opacity-75 text-gray-700 dark:text-gray-200'],
    ['menu-btn', 'flex h-36px w-full items-center px-2 rounded-10px opacity-75 hover:text-sky-400 hover:bg-neutral200 hover:dark:bg-dark'],
    ['pagination-cell', 'flex items-center justify-center p2 min-w-8 bg-neutral-100 hover:bg-neutral-200 dark:bg-dark-700 dark:hover:bg-dark-800 rounded-5px cursor-pointer uppercase tracking-wide'],
  ],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      warn: true,
    }),
    presetTypography(),
    presetWebFonts({
      fonts: {
        sans: 'DM Sans',
        serif: 'DM Serif Display',
        mono: 'DM Mono',
      },
    }),
  ],
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],
  safelist: 'prose prose-sm m-auto text-left'.split(' '),
})
