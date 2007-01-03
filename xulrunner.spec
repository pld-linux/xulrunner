# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
%define		_snap	20070102
%define		_rel	2
#
Summary:	XULRunner - Mozilla Runtime Environment for XUL+XPCOM applications
Summary(pl):	XULRunner - ¶rodowisko uruchomieniowe Mozilli dla aplikacji XUL+XPCOM
Name:		xulrunner
Version:	1.8.1.1
Release:	1.%{_snap}.%{_rel}
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
Source0:	%{name}-%{version}-%{_snap}-source.tar.bz2
# Source0-md5:	92b4936a5b8bd24edac8feaa26d13567
Patch0:		%{name}-ldap-with-nss.patch
Patch1:		%{name}-install.patch
URL:		http://developer.mozilla.org/en/docs/XULRunner
BuildRequires:	/bin/csh
%{?with_gnome:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	freetype-devel >= 1:2.1.8
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	heimdal-devel >= 0.7.1
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnome:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.3
BuildRequires:	nss-devel >= 1:3.11.3-3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xcursor-devel
BuildRequires:	xft-devel >= 2.1-2
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

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
Requires:	nspr-devel >= 1:4.6.3
Requires:	nss-devel >= 1:3.11.3
Obsoletes:	mozilla-devel
Obsoletes:	mozilla-firefox-devel
Obsoletes:	seamonkey-devel

%description devel
XULRunner development package.

%description devel -l pl
Pakiet programistyczny XULRunnera.

%prep
%setup -qc
cd mozilla

%patch0 -p1
%patch1 -p1

%build
cd mozilla

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

export ac_cv_visibility_pragma=no
%configure2_13 \
	%{!?debug:--disable-debug} \
	%{!?with_gnome:--disable-gnomeui} \
	%{!?with_gnome:--disable-gnomevfs} \
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
	--with-default-mozilla-five-home=%{_libdir}/%{name} \
	--with-pthreads \
	--with-system-jpeg \
	--with-system-nspr \
	--with-system-nss \
	--with-system-png \
	--with-system-zlib \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla

%{__make} -C xpinstall/packager make-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

install -d \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/components \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir}} \
	$RPM_BUILD_ROOT{%{_pkgconfigdir},%{_includedir}}

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries $RPM_BUILD_ROOT%{_datadir}/%{name}/dictionaries
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/dictionaries $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res

# files created by regxpcom
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

# header/development files
cp -rfLp dist/include	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfLp dist/idl	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfLp dist/public/ldap{,-private} $RPM_BUILD_ROOT%{_includedir}/%{name}
install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/xpidl $RPM_BUILD_ROOT%{_bindir}/xpidl
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/xpt_dump $RPM_BUILD_ROOT%{_bindir}/xpt_dump
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/xpt_link $RPM_BUILD_ROOT%{_bindir}/xpt_link

for f in build/unix/*.pc ; do
	sed -e 's/xulrunner-%{version}/xulrunner/' $f \
		> $RPM_BUILD_ROOT%{_pkgconfigdir}/$(basename $f)
done

sed -e 's,%{_lib}/xulrunner-%{version},%{_lib},g;s/xulrunner-%{version}/xulrunner/g' build/unix/xulrunner-gtkmozembed.pc \
		> $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-gtkmozembed.pc

# add includir/dom to Cflags, for openvrml.spec, perhaps others
sed -i -e '/Cflags:/{/{includedir}\/dom/!s,$, -I${includedir}/dom,}' $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-plugin.pc

rm $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-nss.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-nspr.pc

# rename to without -bin extension for killall xulrunner to work
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner{-bin,}
cat << 'EOF' > $RPM_BUILD_ROOT%{_bindir}/xulrunner
#!/bin/sh
export LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

exec %{_libdir}/%{name}/xulrunner "$@"
EOF

cat << 'EOF' > $RPM_BUILD_ROOT%{_bindir}/xpcshell
#!/bin/sh
export LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

exec %{_libdir}/%{name}/xpcshell "$@"
EOF

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} %{_libdir}/%{name}/regxpcom

rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post -p %{_sbindir}/%{name}-chrome+xpcom-generate

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

%dir %{_libdir}/%{name}/chrome
%dir %{_libdir}/%{name}/components
%dir %{_libdir}/%{name}/defaults
%dir %{_libdir}/%{name}/dictionaries
%dir %{_libdir}/%{name}/greprefs
%dir %{_libdir}/%{name}/res
%dir %{_datadir}/%{name}

%attr(755,root,root) %{_libdir}/%{name}/xulrunner
%attr(755,root,root) %{_libdir}/%{name}/xpcshell
%attr(755,root,root) %{_libdir}/%{name}/xulrunner-stub
%attr(755,root,root) %{_libdir}/%{name}/reg*

%attr(755,root,root) %{_libdir}/%{name}/components/libauth*.so
%attr(755,root,root) %{_libdir}/%{name}/components/libautoconfig.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcookie.so
%attr(755,root,root) %{_libdir}/%{name}/components/libfileview.so
%{?with_gnome:%attr(755,root,root) %{_libdir}/%{name}/components/libimgicon.so}
%{?with_gnome:%attr(755,root,root) %{_libdir}/%{name}/components/libnkgnomevfs.so}
%attr(755,root,root) %{_libdir}/%{name}/components/libmoz*.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmyspell.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnkdatetime.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnkfinger.so
%attr(755,root,root) %{_libdir}/%{name}/components/libp3p.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpermissions.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpipboot.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpipnss.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpippki.so
%attr(755,root,root) %{_libdir}/%{name}/components/libschemavalidation.so
%attr(755,root,root) %{_libdir}/%{name}/components/libspellchecker.so
%attr(755,root,root) %{_libdir}/%{name}/components/libsql.so
%attr(755,root,root) %{_libdir}/%{name}/components/libsroaming.so
%attr(755,root,root) %{_libdir}/%{name}/components/libsystem-pref.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtransformiix.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtypeaheadfind.so
%attr(755,root,root) %{_libdir}/%{name}/components/libuniversalchardet.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwallet.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwalletviewers.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwebsrvcs.so
%attr(755,root,root) %{_libdir}/%{name}/components/libx*.so

%{_libdir}/%{name}/components/access*.xpt
%{_libdir}/%{name}/components/alerts.xpt
%{_libdir}/%{name}/components/appshell.xpt
%{_libdir}/%{name}/components/appstartup.xpt
%{_libdir}/%{name}/components/autocomplete.xpt
%{_libdir}/%{name}/components/autoconfig.xpt
%{_libdir}/%{name}/components/caps.xpt
%{_libdir}/%{name}/components/chardet.xpt
%{_libdir}/%{name}/components/chrome.xpt
%{_libdir}/%{name}/components/commandhandler.xpt
%{_libdir}/%{name}/components/commandlines.xpt
%{_libdir}/%{name}/components/composer.xpt
%{_libdir}/%{name}/components/content*.xpt
%{_libdir}/%{name}/components/cookie.xpt
%{_libdir}/%{name}/components/directory.xpt
%{_libdir}/%{name}/components/docshell.xpt
%{_libdir}/%{name}/components/downloads.xpt
%{_libdir}/%{name}/components/dom*.xpt
%{_libdir}/%{name}/components/editor.xpt
%{_libdir}/%{name}/components/embed_base.xpt
%{_libdir}/%{name}/components/extensions.xpt
%{_libdir}/%{name}/components/exthandler.xpt
%{_libdir}/%{name}/components/fastfind.xpt
%{_libdir}/%{name}/components/feeds.xpt
%{_libdir}/%{name}/components/find.xpt
%{_libdir}/%{name}/components/filepicker.xpt
%{_libdir}/%{name}/components/gfx*.xpt
%{_libdir}/%{name}/components/history.xpt
%{_libdir}/%{name}/components/htmlparser.xpt
%{?with_gnome:%{_libdir}/%{name}/components/imgicon.xpt}
%{_libdir}/%{name}/components/imglib2.xpt
%{_libdir}/%{name}/components/inspector.xpt
%{_libdir}/%{name}/components/intl.xpt
%{_libdir}/%{name}/components/jar.xpt
%{_libdir}/%{name}/components/js*.xpt
%{_libdir}/%{name}/components/layout*.xpt
%{_libdir}/%{name}/components/locale.xpt
%{_libdir}/%{name}/components/lwbrk.xpt
%{_libdir}/%{name}/components/mimetype.xpt
%{_libdir}/%{name}/components/moz*.xpt
%{_libdir}/%{name}/components/necko*.xpt
%{_libdir}/%{name}/components/oji.xpt
%{_libdir}/%{name}/components/p3p.xpt
%{_libdir}/%{name}/components/passwordmgr.xpt
%{_libdir}/%{name}/components/pipboot.xpt
%{_libdir}/%{name}/components/pipnss.xpt
%{_libdir}/%{name}/components/pippki.xpt
%{_libdir}/%{name}/components/plugin.xpt
%{_libdir}/%{name}/components/pref.xpt
%{_libdir}/%{name}/components/prefetch.xpt
%{_libdir}/%{name}/components/profile.xpt
%{_libdir}/%{name}/components/progressDlg.xpt
%{_libdir}/%{name}/components/proxyObjInst.xpt
%{_libdir}/%{name}/components/rdf.xpt
%{_libdir}/%{name}/components/satchel.xpt
%{_libdir}/%{name}/components/saxparser.xpt
%{_libdir}/%{name}/components/schemavalidation.xpt
%{_libdir}/%{name}/components/shistory.xpt
%{_libdir}/%{name}/components/signonviewer.xpt
%{_libdir}/%{name}/components/spellchecker.xpt
%{_libdir}/%{name}/components/sql.xpt
%{_libdir}/%{name}/components/storage.xpt
%{_libdir}/%{name}/components/toolkitprofile.xpt
%{_libdir}/%{name}/components/toolkitremote.xpt
%{_libdir}/%{name}/components/txmgr.xpt
%{_libdir}/%{name}/components/txtsvc.xpt
%{_libdir}/%{name}/components/typeaheadfind.xpt
%{_libdir}/%{name}/components/uconv.xpt
%{_libdir}/%{name}/components/unicharutil.xpt
%{_libdir}/%{name}/components/update.xpt
%{_libdir}/%{name}/components/uriloader.xpt
%{_libdir}/%{name}/components/urlformatter.xpt
%{_libdir}/%{name}/components/wallet*.xpt
%{_libdir}/%{name}/components/webBrowser_core.xpt
%{_libdir}/%{name}/components/webbrowserpersist.xpt
%{_libdir}/%{name}/components/webshell_idls.xpt
%{_libdir}/%{name}/components/websrvcs.xpt
%{_libdir}/%{name}/components/widget.xpt
%{_libdir}/%{name}/components/windowds.xpt
%{_libdir}/%{name}/components/windowwatcher.xpt
%{_libdir}/%{name}/components/x*.xpt

%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/nsCloseAllWindows.js
%{_libdir}/%{name}/components/nsDefaultCLH.js
%{_libdir}/%{name}/components/nsDictionary.js
%{_libdir}/%{name}/components/nsExtensionManager.js
%{_libdir}/%{name}/components/nsFilePicker.js
%{_libdir}/%{name}/components/nsHelperAppDlg.js
%{_libdir}/%{name}/components/nsInterfaceInfoToIDL.js
%{_libdir}/%{name}/components/nsKillAll.js
%{_libdir}/%{name}/components/nsProgressDialog.js
%{_libdir}/%{name}/components/nsProxyAutoConfig.js
%{_libdir}/%{name}/components/nsResetPref.js
%{_libdir}/%{name}/components/nsSchemaValidatorRegexp.js
%{_libdir}/%{name}/components/nsUpdateService.js
%{_libdir}/%{name}/components/nsURLFormatter.js
%{_libdir}/%{name}/components/nsXmlRpcClient.js
%{_libdir}/%{name}/components/nsXULAppInstall.js

# not *.dat, so check-files can catch any new files
# (and they won't be just silently placed empty in rpm)
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%dir %{_datadir}/%{name}/chrome
%{_datadir}/%{name}/chrome/US.jar
%{_datadir}/%{name}/chrome/classic.jar
%{_datadir}/%{name}/chrome/classic.manifest
%{_datadir}/%{name}/chrome/comm.jar
%{_datadir}/%{name}/chrome/comm.manifest
%{_datadir}/%{name}/chrome/content-packs.jar
%{_datadir}/%{name}/chrome/cview.jar
%{_datadir}/%{name}/chrome/en-US.jar
%{_datadir}/%{name}/chrome/en-US.manifest
%{_datadir}/%{name}/chrome/help.jar
%{_datadir}/%{name}/chrome/modern.jar
%{_datadir}/%{name}/chrome/pippki.jar
%{_datadir}/%{name}/chrome/pippki.manifest
%{_datadir}/%{name}/chrome/reporter.jar
%{_datadir}/%{name}/chrome/reporter.manifest
%{_datadir}/%{name}/chrome/sql.jar
%{_datadir}/%{name}/chrome/sroaming.jar
%{_datadir}/%{name}/chrome/tasks.jar
%{_datadir}/%{name}/chrome/toolkit.jar
%{_datadir}/%{name}/chrome/toolkit.manifest

# not generated automatically ?
%{_datadir}/%{name}/chrome/chromelist.txt

%ghost %{_datadir}/%{name}/chrome/installed-chrome.txt

%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/dictionaries
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/res

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libgtkembedmoz.so
%attr(755,root,root) %{_libdir}/%{name}/libldap50.so
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libprldap50.so
%attr(755,root,root) %{_libdir}/%{name}/libssldap50.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/reg*
%attr(755,root,root) %{_bindir}/xpcshell
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%{_includedir}/%{name}
%{_pkgconfigdir}/*
