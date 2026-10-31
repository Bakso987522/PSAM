import { joinURL } from 'ufo'

export default defineEventHandler((event) => {
  const { apiUrl } = useRuntimeConfig(event)
  const target = joinURL(apiUrl, event.path.replace(/^\/api/, ''))
  return proxyRequest(event, target)
})
