import { joinURL } from 'ufo'
import { toLabelFileName } from '#shared/utils/labelFileName'

const LABEL_ORIGIN = 'https://www.gov.pl/attachment/'

interface ProductCard {
  product: {
    name: string
    label_url: string | null
    label_matched: boolean
  }
}

const dateFormatter = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Warsaw' })

const toAscii = (name: string) =>
  name
    .replace(/ł/g, 'l')
    .replace(/Ł/g, 'L')
    .normalize('NFKD')
    .replace(/[^\w.-]/g, '')

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id') ?? ''
  const { apiUrl } = useRuntimeConfig(event)

  const card = await $fetch<ProductCard>(
    joinURL(apiUrl, 'sor', encodeURIComponent(id)),
  ).catch(() => null)

  const product = card?.product
  if (!product?.label_matched || !product.label_url?.startsWith(LABEL_ORIGIN)) {
    throw createError({ statusCode: 404, statusMessage: 'Label not found' })
  }

  const upstream = await fetch(product.label_url, { redirect: 'follow' }).catch(() => null)
  if (!upstream?.ok || !upstream.body) {
    throw createError({ statusCode: 502, statusMessage: 'Label unavailable' })
  }

  const download = Boolean(getQuery(event).download)
  const fileName = toLabelFileName(product.name, dateFormatter.format(new Date()))

  setResponseHeaders(event, {
    'Content-Type': 'application/pdf',
    'Content-Disposition': `${download ? 'attachment' : 'inline'}; filename="${toAscii(fileName)}"; filename*=UTF-8''${encodeURIComponent(fileName)}`,
    'Cache-Control': download ? 'no-store' : 'public, max-age=86400',
    ...(upstream.headers.get('content-length')
      ? { 'Content-Length': upstream.headers.get('content-length')! }
      : {}),
  })

  return sendStream(event, upstream.body)
})
