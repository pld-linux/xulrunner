Summary:	XULRunner - Mozilla Runtime Environment for XUL+XPCOM applications
Summary(pl):	XULRunner - ¶rodowisko uruchomieniowe Mozilli dla aplikacji XUL+XPCOM
Name:		xulrunner
Version:	1.8.0.4
Release:	0.2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
Source0:	http://ftp.mozilla.org/pub/mozilla.org/xulrunner/releases/%{version}/source/%{name}-%{version}-source.tar.bz2
# Source0-md5:	4dc09831aa4e94fda5182a4897ed08e9
Patch0:		%{name}-nss.patch
Patch1:		%{name}-ldap-with-nss.patch
Patch2:		%{name}-nsIPermission.patch
Patch3:		%{name}-nsISidebar.patch
URL:		http://developer.mozilla.org/en/docs/XULRunner
BuildRequires:	/bin/csh
BuildRequires:	/bin/ex
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.1
BuildRequires:	nss-devel >= 3.10.2
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 1:5.6.0
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.15.1
BuildRequires:	xcursor-devel
BuildRequires:	xft-devel >= 2.1-2
BuildRequires:	zip >= 2.1
BuildRequires:	zlib-devel >= 1.2.3
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%{?with_svg:Requires:	cairo >= 1.0.0}
Requires:	nspr >= 1:4.6.1
Requires:	nss >= 3.10.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

%define		_xulrunnerdir	%{_libdir}/%{name}
%define		_chromedir	%{_libdir}/%{name}/chrome
# mozilla, seamonkey and firefox provide their own versions
%define		_noautoreqdep	libgtkembedmoz.so libldap50.so libmozjs.so libprldap50.so libssldap50.so libxpcom.so

%description
XULRunner is a Mozilla runtime package that can be used to bootstrap
XUL+XPCOM applications that are as rich as Firefox and Thunderbird. It
will provide mechanisms for installing, upgrading, and uninstalling
these applications. XULRunner will also provide libxul, a solution
which allows the embedding of Mozilla technologies in other projects
and products.

%description -l pl
XULRunner to pakiet uruchomieniowy Mozilli, którego mo¿na u¿yæ do
uruchamiania aplikacji XUL+XPCOM, nawet takich jak Firefox czy
Thunderbird. Udostêpni mechanizmy do instalowania, uaktualniania i
odinstalowywania tych aplikacji. XULRunner bêdzie tak¿e dostarcza³
libxul - rozwi±zanie umo¿liwiaj±ce osadzanie technologii Mozilli w
innych projektach i produktach.

%package libs
Summary:	XULRunner shared libraries
Summary(pl):	Biblioteki wspó³dzielone XULRunnera
Group:		X11/Libraries

%description libs
XULRunner shared libraries.

%description libs -l pl
Biblioteki wspó³dzielone XULRunnera.

%package devel
Summary:	Headers for developing programs that will use XULRunner
Summary(pl):	Pliki nag³ówkowe do tworzenia programów u¿ywaj±cych XULRunnera
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.1
Obsoletes:	mozilla-devel
Obsoletes:	mozilla-firefox-devel
Obsoletes:	seamonkey-devel

%description devel
XULRunner development package.

%description devel -l pl
Pakiet programistyczny XULRunnera.

%prep
%setup -q -c -T
tar jxf %{SOURCE0} --strip-components=1

%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0

%build
BUILD_OFFICIAL="1"; export BUILD_OFFICIAL
MOZILLA_OFFICIAL="1"; export MOZILLA_OFFICIAL

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf
export ac_cv_visibility_pragma=no
%configure2_13 \
	%{!?debug:--disable-debug} \
	--disable-elf-dynstr-gc \
	%{!?with_gnomeui:--disable-gnomeui} \
	%{!?with_gnomevfs:--disable-gnomevfs} \
	--disable-javaxpcom \
	--disable-mailnews \
	--disable-pedantic \
	--disable-tests \
	--disable-xterm-updates \
	--enable-application=xulrunner \
	--enable-crypto \
	--enable-default-toolkit=gtk2 \
	--enable-extensions \
	--enable-ldap \
	--enable-mathml \
	--enable-optimize="%{rpmcflags}" \
	--enable-postscript \
	%{!?debug:--enable-strip} \
	--enable-xft \
	--enable-xinerama \
	--enable-xprint \
	--enable-old-abi-compat-wrappers \
	--with-default-mozilla-five-home=%{_xulrunnerdir} \
	--with-pthreads \
	--with-system-jpeg \
	--with-system-nspr \
	--with-system-png \
	--with-system-zlib \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_datadir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/{chrome,defaults,greprefs,myspell,res} \
	$RPM_BUILD_ROOT%{_xulrunnerdir}/components \
	$RPM_BUILD_ROOT{%{_includedir}/%{name}/idl,%{_pkgconfigdir}}

# preparing to create register
# remove empty directory trees
rm -fr dist/bin/chrome/{US,chatzilla,classic,comm,content-packs,cview,embed,embed-sample,en-US,en-mac,en-unix,en-win,help,inspector,messenger,modern,pipnss,pippki,toolkit,venkman,xmlterm}
# non-unix
rm -f dist/bin/chrome/en-{mac,win}.jar

# creating and installing register
LD_LIBRARY_PATH="dist/bin" MOZILLA_FIVE_HOME="dist/bin" dist/bin/regxpcom
#install dist/bin/component.reg $RPM_BUILD_ROOT%{_xulrunnerdir}

ln -sf ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_chromedir}
ln -sf ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_xulrunnerdir}/defaults
ln -sf ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_xulrunnerdir}/greprefs
#ln -sf ../../share/%{name}/icons $RPM_BUILD_ROOT%{_xulrunnerdir}/icons
ln -sf ../../share/%{name}/res $RPM_BUILD_ROOT%{_xulrunnerdir}/res
#ln -sf ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_xulrunnerdir}/searchplugins
ln -sf ../../../share/%{name}/myspell $RPM_BUILD_ROOT%{_xulrunnerdir}/components/myspell

cp -frL dist/bin/chrome/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
cp -frL dist/bin/components/{[!m],m[!y]}*	$RPM_BUILD_ROOT%{_xulrunnerdir}/components
cp -frL dist/bin/components/myspell/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/myspell
cp -frL dist/bin/defaults/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
cp -frL dist/bin/res/*		$RPM_BUILD_ROOT%{_datadir}/%{name}/res
cp -frL dist/gre/greprefs/*	$RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
cp -frL dist/idl/*		$RPM_BUILD_ROOT%{_includedir}/%{name}/idl
cp -frL dist/include/*		$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -frL dist/public/ldap{,-private} $RPM_BUILD_ROOT%{_includedir}/%{name}

install dist/bin/*.so $RPM_BUILD_ROOT%{_xulrunnerdir}

ln -s %{_libdir}/libnssckbi.so $RPM_BUILD_ROOT%{_xulrunnerdir}/libnssckbi.so

for f in build/unix/*.pc ; do
	sed -e 's/xulrunner-%{version}/xulrunner/' $f \
		> $RPM_BUILD_ROOT%{_pkgconfigdir}/$(basename $f)
done

sed -e 's,lib/xulrunner-%{version},lib,g;s/xulrunner-%{version}/xulrunner/g' build/unix/xulrunner-gtkmozembed.pc \
		> $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-gtkmozembed.pc

# add includir/dom to Cflags, for openvrml.spec, perhaps others
sed -i -e '/Cflags:/{/{includedir}\/dom/!s,$, -I${includedir}/dom,}' $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-plugin.pc

rm -f $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-nss.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-nspr.pc

install dist/bin/xulrunner-bin $RPM_BUILD_ROOT%{_xulrunnerdir}
install dist/bin/regxpcom $RPM_BUILD_ROOT%{_xulrunnerdir}
install dist/bin/xpidl $RPM_BUILD_ROOT%{_xulrunnerdir}
install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpidl $RPM_BUILD_ROOT%{_bindir}

cp $RPM_BUILD_ROOT%{_chromedir}/installed-chrome.txt \
        $RPM_BUILD_ROOT%{_chromedir}/%{name}-installed-chrome.txt

cat << 'EOF' > $RPM_BUILD_ROOT%{_bindir}/xulrunner
#!/bin/sh

LD_LIBRARY_PATH=/usr/lib/xulrunner${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

MOZILLA_FIVE_HOME=/usr/lib/xulrunner
/usr/lib/xulrunner/xulrunner-bin "$@"
EOF

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
cd %{_datadir}/%{name}/chrome
cat *-installed-chrome.txt > installed-chrome.txt
rm -f chrome.rdf overlays.rdf
rm -f %{_xulrunnerdir}/components/{compreg,xpti}.dat

LD_LIBRARY_PATH=%{_xulrunnerdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

MOZILLA_FIVE_HOME=%{_xulrunnerdir} %{_xulrunnerdir}/regxpcom
exit 0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/%{name}-chrome+xpcom-generate

%postun
if [ "$1" = "1" ]; then
	%{_sbindir}/%{name}-chrome+xpcom-generate
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xulrunner
%attr(744,root,root) %{_sbindir}/%{name}-chrome+xpcom-generate

%dir %{_xulrunnerdir}
%dir %{_chromedir}
%dir %{_xulrunnerdir}/components
%dir %{_xulrunnerdir}/defaults
%dir %{_xulrunnerdir}/greprefs
#%dir %{_xulrunnerdir}/icons
#%dir %{_xulrunnerdir}/plugins
%dir %{_xulrunnerdir}/res
%dir %{_datadir}/%{name}

%attr(755,root,root) %{_xulrunnerdir}/xulrunner-bin
%attr(755,root,root) %{_xulrunnerdir}/reg*
%attr(755,root,root) %{_xulrunnerdir}/xpidl

%attr(755,root,root) %{_xulrunnerdir}/libnssckbi.so

%attr(755,root,root) %{_xulrunnerdir}/components/libauth*.so
%attr(755,root,root) %{_xulrunnerdir}/components/libautoconfig.so
%attr(755,root,root) %{_xulrunnerdir}/components/libcookie.so
%attr(755,root,root) %{_xulrunnerdir}/components/libfileview.so
%attr(755,root,root) %{_xulrunnerdir}/components/libmoz*.so
%attr(755,root,root) %{_xulrunnerdir}/components/libmyspell.so
%attr(755,root,root) %{_xulrunnerdir}/components/libnkdatetime.so
%attr(755,root,root) %{_xulrunnerdir}/components/libnkfinger.so
%attr(755,root,root) %{_xulrunnerdir}/components/libp3p.so
%attr(755,root,root) %{_xulrunnerdir}/components/libpermissions.so
%attr(755,root,root) %{_xulrunnerdir}/components/libpipboot.so
%attr(755,root,root) %{_xulrunnerdir}/components/libpipnss.so
%attr(755,root,root) %{_xulrunnerdir}/components/libpippki.so
%attr(755,root,root) %{_xulrunnerdir}/components/libschemavalidation.so
%attr(755,root,root) %{_xulrunnerdir}/components/libspellchecker.so
%attr(755,root,root) %{_xulrunnerdir}/components/libsql.so
%attr(755,root,root) %{_xulrunnerdir}/components/libsroaming.so
%attr(755,root,root) %{_xulrunnerdir}/components/libsystem-pref.so
%attr(755,root,root) %{_xulrunnerdir}/components/libtransformiix.so
%attr(755,root,root) %{_xulrunnerdir}/components/libtypeaheadfind.so
%attr(755,root,root) %{_xulrunnerdir}/components/libuniversalchardet.so
%attr(755,root,root) %{_xulrunnerdir}/components/libwallet.so
%attr(755,root,root) %{_xulrunnerdir}/components/libwalletviewers.so
%attr(755,root,root) %{_xulrunnerdir}/components/libwebsrvcs.so
%attr(755,root,root) %{_xulrunnerdir}/components/libx*.so

%{_xulrunnerdir}/components/access*.xpt
%{_xulrunnerdir}/components/alerts.xpt
%{_xulrunnerdir}/components/appshell.xpt
%{_xulrunnerdir}/components/appstartup.xpt
%{_xulrunnerdir}/components/autocomplete.xpt
%{_xulrunnerdir}/components/autoconfig.xpt
%{_xulrunnerdir}/components/caps.xpt
%{_xulrunnerdir}/components/chardet.xpt
%{_xulrunnerdir}/components/chrome.xpt
%{_xulrunnerdir}/components/commandhandler.xpt
%{_xulrunnerdir}/components/commandlines.xpt
%{_xulrunnerdir}/components/composer.xpt
%{_xulrunnerdir}/components/content*.xpt
%{_xulrunnerdir}/components/cookie.xpt
%{_xulrunnerdir}/components/directory.xpt
%{_xulrunnerdir}/components/docshell.xpt
%{_xulrunnerdir}/components/downloads.xpt
%{_xulrunnerdir}/components/dom*.xpt
%{_xulrunnerdir}/components/editor.xpt
%{_xulrunnerdir}/components/embed_base.xpt
%{_xulrunnerdir}/components/extensions.xpt
%{_xulrunnerdir}/components/exthandler.xpt
%{_xulrunnerdir}/components/fastfind.xpt
%{_xulrunnerdir}/components/find.xpt
%{_xulrunnerdir}/components/filepicker.xpt
%{_xulrunnerdir}/components/gfx*.xpt
%{?with_svg:%{_xulrunnerdir}/components/gksvgrenderer.xpt}
%{_xulrunnerdir}/components/history.xpt
%{_xulrunnerdir}/components/htmlparser.xpt
%{?with_gnomeui:%{_xulrunnerdir}/components/imgicon.xpt}
%{_xulrunnerdir}/components/imglib2.xpt
%{_xulrunnerdir}/components/intl.xpt
%{_xulrunnerdir}/components/jar.xpt
%{_xulrunnerdir}/components/js*.xpt
%{_xulrunnerdir}/components/layout*.xpt
%{_xulrunnerdir}/components/locale.xpt
%{_xulrunnerdir}/components/lwbrk.xpt
%{_xulrunnerdir}/components/mimetype.xpt
%{_xulrunnerdir}/components/moz*.xpt
%{_xulrunnerdir}/components/necko*.xpt
%{_xulrunnerdir}/components/oji.xpt
%{_xulrunnerdir}/components/p3p.xpt
%{_xulrunnerdir}/components/passwordmgr.xpt
%{_xulrunnerdir}/components/pipboot.xpt
%{_xulrunnerdir}/components/pipnss.xpt
%{_xulrunnerdir}/components/pippki.xpt
%{_xulrunnerdir}/components/plugin.xpt
%{_xulrunnerdir}/components/pref.xpt
%{_xulrunnerdir}/components/prefetch.xpt
%{_xulrunnerdir}/components/profile.xpt
%{_xulrunnerdir}/components/progressDlg.xpt
%{_xulrunnerdir}/components/proxyObjInst.xpt
%{_xulrunnerdir}/components/rdf.xpt
%{_xulrunnerdir}/components/satchel.xpt
%{_xulrunnerdir}/components/schemavalidation.xpt
%{_xulrunnerdir}/components/shistory.xpt
%{_xulrunnerdir}/components/signonviewer.xpt
%{_xulrunnerdir}/components/spellchecker.xpt
%{_xulrunnerdir}/components/sql.xpt
%{_xulrunnerdir}/components/toolkitprofile.xpt
%{_xulrunnerdir}/components/toolkitremote.xpt
%{_xulrunnerdir}/components/txmgr.xpt
%{_xulrunnerdir}/components/txtsvc.xpt
%{_xulrunnerdir}/components/typeaheadfind.xpt
%{_xulrunnerdir}/components/uconv.xpt
%{_xulrunnerdir}/components/unicharutil.xpt
%{_xulrunnerdir}/components/update.xpt
%{_xulrunnerdir}/components/uriloader.xpt
%{_xulrunnerdir}/components/wallet*.xpt
%{_xulrunnerdir}/components/webBrowser_core.xpt
%{_xulrunnerdir}/components/webbrowserpersist.xpt
%{_xulrunnerdir}/components/webshell_idls.xpt
%{_xulrunnerdir}/components/websrvcs.xpt
%{_xulrunnerdir}/components/widget.xpt
%{_xulrunnerdir}/components/windowds.xpt
%{_xulrunnerdir}/components/windowwatcher.xpt
%{_xulrunnerdir}/components/x*.xpt

%{_xulrunnerdir}/components/jsconsole-clhandler.js
%{_xulrunnerdir}/components/nsCloseAllWindows.js
%{_xulrunnerdir}/components/nsDefaultCLH.js
%{_xulrunnerdir}/components/nsDictionary.js
%{_xulrunnerdir}/components/nsExtensionManager.js
%{_xulrunnerdir}/components/nsFilePicker.js
%{_xulrunnerdir}/components/nsHelperAppDlg.js
%{_xulrunnerdir}/components/nsInterfaceInfoToIDL.js
%{_xulrunnerdir}/components/nsKillAll.js
%{_xulrunnerdir}/components/nsProgressDialog.js
%{_xulrunnerdir}/components/nsProxyAutoConfig.js
%{_xulrunnerdir}/components/nsResetPref.js
%{_xulrunnerdir}/components/nsSchemaValidatorRegexp.js
%{_xulrunnerdir}/components/nsUpdateService.js
%{_xulrunnerdir}/components/nsXmlRpcClient.js
%{_xulrunnerdir}/components/nsXULAppInstall.js

# not *.dat, so check-files can catch any new files
# (and they won't be just silently placed empty in rpm)
%ghost %{_xulrunnerdir}/components/compreg.dat
%ghost %{_xulrunnerdir}/components/xpti.dat

%{_xulrunnerdir}/components/myspell

%dir %{_datadir}/%{name}/chrome
%{_datadir}/%{name}/chrome/US.jar
%{_datadir}/%{name}/chrome/classic.jar
%{_datadir}/%{name}/chrome/comm.jar
%{_datadir}/%{name}/chrome/content-packs.jar
%{_datadir}/%{name}/chrome/cview.jar
%{_datadir}/%{name}/chrome/en-US.jar
%{_datadir}/%{name}/chrome/help.jar
%{_datadir}/%{name}/chrome/modern.jar
%{_datadir}/%{name}/chrome/pippki.jar
%{_datadir}/%{name}/chrome/reporter.jar
%{_datadir}/%{name}/chrome/sql.jar
%{_datadir}/%{name}/chrome/sroaming.jar
%{_datadir}/%{name}/chrome/tasks.jar
%{_datadir}/%{name}/chrome/toolkit.jar

# not generated automatically ?
%{_datadir}/%{name}/chrome/chromelist.txt
#%{_datadir}/%{name}/chrome/icons

%{_datadir}/%{name}/chrome/%{name}-installed-chrome.txt
%ghost %{_datadir}/%{name}/chrome/installed-chrome.txt

%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
#%{_datadir}/%{name}/icons
%{_datadir}/%{name}/myspell
%{_datadir}/%{name}/res

%files libs
%defattr(644,root,root,755)
# libxpcom.so used by mozillaplug-in
# probably should add more if more packages require
%attr(755,root,root) %{_xulrunnerdir}/libxpcom.so

# add rest too
%attr(755,root,root) %{_xulrunnerdir}/libxul.so
%attr(755,root,root) %{_xulrunnerdir}/libgtkembedmoz.so
%attr(755,root,root) %{_xulrunnerdir}/libldap50.so
%attr(755,root,root) %{_xulrunnerdir}/libprldap50.so
%attr(755,root,root) %{_xulrunnerdir}/libssldap50.so
%attr(755,root,root) %{_xulrunnerdir}/libmozjs.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/reg*
%attr(755,root,root) %{_bindir}/xpidl
%{_includedir}/%{name}
%{_pkgconfigdir}/*
