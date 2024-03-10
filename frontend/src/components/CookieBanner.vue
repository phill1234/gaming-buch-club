<template>
  <span></span>
</template>
<script setup lang="js">
(function(window, document, dataLayerName, id) {
  (window[dataLayerName] = window[dataLayerName] || [])
  window[dataLayerName].push({
    start: new Date().getTime(),
    event: 'stg.start'
  })
  const scripts = document.getElementsByTagName('script')[0],
    tags = document.createElement('script')

  function stgCreateCookie(a, b, c) {
    let d = ''
    let f
    if (c) {
      const e = new Date()
      e.setTime(e.getTime() + 24 * c * 60 * 60 * 1e3);
      (d = '; expires=' + e.toUTCString())
      f = '; SameSite=Strict'
    }
    document.cookie = a + '=' + b + d + f + '; path=/'
  }

  const isStgDebug =
    (window.location.href.match('stg_debug') ||
      document.cookie.match('stg_debug')) &&
    !window.location.href.match('stg_disable_debug')
  stgCreateCookie('stg_debug', isStgDebug ? 1 : '', isStgDebug ? 14 : -1)
  const qP = []
  dataLayerName !== 'dataLayer' && qP.push('data_layer_name=' + dataLayerName)
  isStgDebug && qP.push('stg_debug')
  const qPString = qP.length > 0 ? '?' + qP.join('&') : '';
  (tags.async = !0);
  (tags.src =
    'https://philipp-lein.containers.piwik.pro/' + id + '.js' + qPString)
  scripts.parentNode.insertBefore(tags, scripts)
  !(function(a, n, i) {
    a[n] = a[n] || {}
    for (let c = 0; c < i.length; c++)
      !(function(i) {
        (a[n][i] = a[n][i] || {});
        (a[n][i].api = a[n][i].api || function() {
            // eslint-disable-next-line prefer-rest-params
            const a = [].slice.call(arguments, 0)
            'string' == typeof a[0] &&
            window[dataLayerName].push({
              event: n + '.' + i + ':' + a[0],
              // eslint-disable-next-line prefer-rest-params
              parameters: [].slice.call(arguments, 1)
            })
          });
      })(i[c])
  })(window, 'ppms', ['tm', 'cm'])
})(window, document, 'dataLayer', 'e34c01f7-e748-46c2-9461-a0f5b605bac0')
</script>

<style scoped></style>
