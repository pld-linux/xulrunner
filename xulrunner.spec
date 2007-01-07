# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
%define		_snap	20070102
%define		_rel	2.7
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
Patch2:		%{name}-pc.patch
Patch3:		%{name}-rpath.patch
URL:		http://developer.mozilla.org/en/docs/XULRunner
BuildRequires:	/bin/csh
%{?with_gnome:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	bzip2-devel
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

rm -rf mozilla/modules/libbz2

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd mozilla

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/xulrunner/config/mozconfig

# Options for 'configure' (same as command-line options).
ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags}"
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnome}
ac_add_options --enable-gnomevfs
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomevfs
ac_add_options --disable-gnomeui
%endif
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-system-cairo
ac_add_options --enable-xft
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}

ac_add_options --disable-mailnews
ac_add_options --disable-pedantic
ac_add_options --disable-xterm-updates
ac_add_options --enable-crypto
ac_add_options --enable-extensions
ac_add_options --enable-ldap
ac_add_options --enable-mathml
ac_add_options --enable-postscript
ac_add_options --enable-xinerama
ac_add_options --enable-xprint
ac_add_options --with-pthreads
ac_add_options --with-x
ac_cv_visibility_pragma=no
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

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

%{__make} -C build/unix install \
	DESTDIR=$RPM_BUILD_ROOT

# we use system pkgs
rm $RPM_BUILD_ROOT%{_pkgconfigdir}/xulrunner-{nspr,nss}.pc

# rpath is used, can move to bindir
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/xulrunner-bin,%{_bindir}/xulrunner}
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/xpcshell,%{_bindir}}

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

%attr(755,root,root) %{_libdir}/%{name}/regxpcom

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

# do not use *.dat here, so check-files can catch any new files
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
#%{_datadir}/%{name}/chrome/chromelist.txt

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
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpcshell
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%attr(755,root,root) %{_libdir}/%{name}/xulrunner-stub
%{_includedir}/%{name}
%{_pkgconfigdir}/*
