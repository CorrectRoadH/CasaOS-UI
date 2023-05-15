#! /usr/bin/env python3
from os import environ, makedirs

project_url = "https://github.com/IceWhaleTech/CasaOS-UI"
release_tag = environ.get('RELEASE_TAG')

content = f"""pkgname=casaos-ui
pkgver={release_tag}
pkgrel=1
pkgdesc="The front-end of CasaOS,build with VueJS."
arch=('any')
url="https://github.com/IceWhaleTech/CasaOS-UI"
license=('unknown')
groups=('casaos')
"""

content += """source=(
    ${url}/releases/download/v${pkgver}/linux-all-casaos-v${pkgver}.tar.gz
)
sha256sums=(SKIP)
package() \{
    _sysdir="${srcdir}/build/sysroot"
    mkdir -p "${pkgdir}/var/lib/casaos"
    mv "${_sysdir}/var/lib/casaos/www" "${pkgdir}/var/lib/casaos/"
}
"""

makedirs('./pkgbuild/casaos-ui', exist_ok=True)
with open('./pkgbuild/casaos-ui/PKGBUILD', 'w') as pkgbuild:
  pkgbuild.write(content)
