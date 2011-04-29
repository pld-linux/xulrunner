#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnome		# synonym for gnomeui (gconf, libnotify and gio are still enabled)
%bcond_with	qt		# build with qt toolkit

%if %{without gnome}
%undefine	with_gnomeui
%endif

# On updating version, grab CVE links from:
# https://www.mozilla.org/security/known-vulnerabilities/firefox36.html#firefox3.6.14

# convert firefox release number to platform version: 4.0.x -> 2.0.x
%define		xulrunner_main	2.0
%define		firefox_ver	4.0.1
%define		xulrunner_ver	%(v=%{firefox_ver}; echo %{xulrunner_main}${v#4.0})

# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)

Summary:	XULRunner - Mozilla Runtime Environment for XUL+XPCOM applications
Summary(pl.UTF-8):	XULRunner - środowisko uruchomieniowe Mozilli dla aplikacji XUL+XPCOM
Name:		xulrunner
Version:	%{xulrunner_ver}
Release:	1.1
Epoch:		2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
# Source tarball for xulrunner is in fact firefox tarball (checked on 1.9), so lets use it
# instead of waiting for mozilla to copy file on ftp.
Source0:	http://releases.mozilla.org/pub/mozilla.org/firefox/releases/%{firefox_ver}/source/firefox-%{firefox_ver}.source.tar.bz2
# Source0-md5:	9abda7d23151e97913c8555a64c13f34
Patch0:		%{name}-install.patch
Patch1:		%{name}-rpath.patch
Patch3:		%{name}-gcc3.patch
Patch4:		%{name}-nss_cflags.patch
Patch5:		%{name}-paths.patch
Patch6:		%{name}-pc.patch
Patch7:		%{name}-prefs.patch
Patch8:		%{name}-ssl_oldapi.patch
Patch9:		%{name}-ppc.patch
URL:		http://developer.mozilla.org/en/docs/XULRunner
%{!?with_qt:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	glib2-devel >= 1:2.16.0
%{!?with_qt:BuildRequires:	gtk+2-devel >= 2:2.10.0}
BuildRequires:	hunspell-devel >= 1.2.3
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libdnet-devel
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libiw-devel
BuildRequires:	libjpeg-devel >= 6b
%{!?with_qt:BuildRequires:	libnotify-devel >= 0.4}
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.2.17
BuildRequires:	libstdc++-devel
BuildRequires:  libvpx-devel
BuildRequires:	nspr-devel >= 1:4.8.7
BuildRequires:	nss-devel >= 1:3.12.9
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.7.5-2
BuildRequires:	startup-notification-devel >= 0.8
%if "%{pld_release}" == "ac"
BuildRequires:	xcursor-devel
BuildRequires:	xft-devel >= 2.1-2
%else
BuildRequires:  xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
%endif
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	myspell-common
Requires:	nspr >= 1:4.8.7
Requires:	nss >= 1:3.12.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp	-D_FORTIFY_SOURCE=[0-9]+

%define		specflags	-fno-strict-aliasing

# no Provides from private modules (don't use %{name} here, it expands to each subpackage name...)
%define		_noautoprovfiles	%{_libdir}/xulrunner/components %{_libdir}/xulrunner/plugins
# no need to require them (we have strict deps for these)
%define		_noautoreq		libmozjs.so libxpcom.so libxul.so

%description
XULRunner is a Mozilla runtime package that can be used to bootstrap
XUL+XPCOM applications that are as rich as Firefox and Thunderbird. It
will provide mechanisms for installing, upgrading, and uninstalling
these applications. XULRunner will also provide libxul, a solution
which allows the embedding of Mozilla technologies in other projects
and products.

%description -l pl.UTF-8
XULRunner to pakiet uruchomieniowy Mozilli, którego można użyć do
uruchamiania aplikacji XUL+XPCOM, nawet takich jak Firefox czy
Thunderbird. Udostępni mechanizmy do instalowania, uaktualniania i
odinstalowywania tych aplikacji. XULRunner będzie także dostarczał
libxul - rozwiązanie umożliwiające osadzanie technologii Mozilli w
innych projektach i produktach.

%package libs
Summary:	XULRunner shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone XULRunnera
Group:		X11/Libraries
Requires:	cairo >= 1.10.2-5
Requires:	dbus-glib >= 0.60
%{!?with_qt:Requires:	gtk+2 >= 2:2.10.0}
Requires:	libpng >= 1.2.17
Requires:	libpng(APNG) >= 0.10
Requires:	pango >= 1:1.14.0
Requires:	sqlite3 >= %{sqlite_build_version}
Requires:	startup-notification >= 0.8

%description libs
XULRunner shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone XULRunnera.

%package devel
Summary:	Headers for developing programs that will use XULRunner
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów używających XULRunnera
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.8.7
Requires:	nss-devel >= 1:3.12.9
Obsoletes:	mozilla-devel
Obsoletes:	mozilla-firefox-devel
Obsoletes:	seamonkey-devel

%description devel
XULRunner development package.

%description devel -l pl.UTF-8
Pakiet programistyczny XULRunnera.

%package gnome
Summary:	GNOME support package for XULRunner
Summary(pl.UTF-8):	Pakiet wspierający integrację XULRunnera z GNOME
Group:		X11/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description gnome
GNOME support package for XULRunner. It integrates GConf, GIO,
libnotify%{?with_gnomeui: and GNOME UI}.

%description gnome -l pl.UTF-8
Pakiet wspierający integrację XULRunnera z GNOME. Obejmuje komponenty
GConf, GIO, libnotify%{?with_gnomeui: oraz GNOME UI}.

%prep
%setup -qc
mv -f mozilla-%{xulrunner_main} mozilla
cd mozilla
# avoid using included headers (-I. is before HUNSPELL_CFLAGS)
%{__rm} extensions/spellcheck/hunspell/src/{*.hxx,hunspell.h}
# hunspell needed for factory including mozHunspell.h
echo 'LOCAL_INCLUDES += $(MOZ_HUNSPELL_CFLAGS)' >> extensions/spellcheck/src/Makefile.in

%patch0 -p1
%patch1 -p1
%if "%{cc_version}" < "3.4"
#%%patch3 -p2
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build

if [ "$(grep -E '^[0-9]\.' mozilla/config/milestone.txt)" != "%{version}" ]; then
	echo >&2
	echo "Version %{version} does not match mozilla/config/milestone.txt!" >&2
	echo >&2
	exit 1
fi

cd mozilla
cp -a %{_datadir}/automake/config.* build/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/xulrunner/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

# Options for 'configure' (same as command-line options).
ac_add_options --build=%{_target_platform}
ac_add_options --host=%{_target_platform}
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
ac_add_options --disable-debug-modules
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
ac_add_options --disable-strip
ac_add_options --disable-strip-libs
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
ac_add_options --disable-gnomevfs
ac_add_options --disable-crashreporter
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
%if %{with qt}
ac_add_options --enable-default-toolkit=cairo-qt
%else
ac_add_options --enable-default-toolkit=cairo-gtk2
%endif
ac_add_options --enable-gio
ac_add_options --enable-libxul
ac_add_options --enable-pango
ac_add_options --enable-shared-js
ac_add_options --enable-startup-notification
ac_add_options --enable-system-cairo
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-libvpx
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --disable-pedantic
ac_add_options --disable-xterm-updates
ac_add_options --enable-extensions="default,cookie,permissions,spellcheck"
ac_add_options --with-x
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla

%{__make} -C obj-%{_target_cpu}/xulrunner/installer install \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	INSTALL_SDK=1 \
	PKG_SKIP_STRIP=1

install -d \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/components \
	$RPM_BUILD_ROOT%{_sbindir}

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/modules $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/modules $RPM_BUILD_ROOT%{_libdir}/%{name}/modules
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

# files created by regxpcom
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

%{__make} -C obj-%{_target_cpu}/build/unix install \
	DESTDIR=$RPM_BUILD_ROOT

# act like "xulrunner --register-global" was run
mv $RPM_BUILD_ROOT/etc/gre.d/%{version}{.system,}.conf

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

# remove unecessary stuff
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/xulrunner
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/LICENSE
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/README.txt
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xulrunner
%attr(755,root,root) %{_libdir}/%{name}/xulrunner-bin

%dir %{_sysconfdir}/gre.d
%{_sysconfdir}/gre.d/%{version}.conf

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/modules
%{_libdir}/%{name}/res

%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/components

%{_libdir}/%{name}/chrome.manifest
%{_libdir}/%{name}/greprefs.js

%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/js
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/nsinstall
%attr(755,root,root) %{_libdir}/%{name}/plugin-container

%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so

%{_libdir}/%{name}/components/accessibility*.xpt
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
%{_libdir}/%{name}/components/content_*.xpt
%{_libdir}/%{name}/components/cookie.xpt
%{_libdir}/%{name}/components/directory.xpt
%{_libdir}/%{name}/components/docshell.xpt
%{_libdir}/%{name}/components/dom*.xpt
%{_libdir}/%{name}/components/downloads.xpt
%{_libdir}/%{name}/components/editor.xpt
%{_libdir}/%{name}/components/embed_base.xpt
%{_libdir}/%{name}/components/extensions.xpt
%{_libdir}/%{name}/components/exthandler.xpt
%{_libdir}/%{name}/components/exthelper.xpt
%{_libdir}/%{name}/components/fastfind.xpt
%{_libdir}/%{name}/components/feeds.xpt
%{_libdir}/%{name}/components/filepicker.xpt
%{_libdir}/%{name}/components/find.xpt
%{_libdir}/%{name}/components/gfx*.xpt
%{_libdir}/%{name}/components/htmlparser.xpt
%{_libdir}/%{name}/components/imgicon.xpt
%{_libdir}/%{name}/components/imglib2.xpt
%{_libdir}/%{name}/components/inspector.xpt
%{_libdir}/%{name}/components/intl.xpt
%{_libdir}/%{name}/components/jar.xpt
%{_libdir}/%{name}/components/jetpack.xpt
%{_libdir}/%{name}/components/js*.xpt
%{_libdir}/%{name}/components/layout*.xpt
%{_libdir}/%{name}/components/locale.xpt
%{_libdir}/%{name}/components/loginmgr.xpt
%{_libdir}/%{name}/components/lwbrk.xpt
%{_libdir}/%{name}/components/mimetype.xpt
%{_libdir}/%{name}/components/moz*.xpt
%{_libdir}/%{name}/components/necko*.xpt
%{_libdir}/%{name}/components/parentalcontrols.xpt
%{_libdir}/%{name}/components/pipboot.xpt
%{_libdir}/%{name}/components/pipnss.xpt
%{_libdir}/%{name}/components/pippki.xpt
%{_libdir}/%{name}/components/places.xpt
%{_libdir}/%{name}/components/plugin.xpt
%{_libdir}/%{name}/components/pref.xpt
%{_libdir}/%{name}/components/prefetch.xpt
%{_libdir}/%{name}/components/profile.xpt
%{_libdir}/%{name}/components/proxyObject.xpt
%{_libdir}/%{name}/components/rdf.xpt
%{_libdir}/%{name}/components/satchel.xpt
%{_libdir}/%{name}/components/saxparser.xpt
%{_libdir}/%{name}/components/services-crypto-component.xpt
%{_libdir}/%{name}/components/shistory.xpt
%{_libdir}/%{name}/components/spellchecker.xpt
%{_libdir}/%{name}/components/startupcache.xpt
%{_libdir}/%{name}/components/storage.xpt
%{_libdir}/%{name}/components/toolkitprofile.xpt
%{_libdir}/%{name}/components/toolkitremote.xpt
%{_libdir}/%{name}/components/txmgr.xpt
%{_libdir}/%{name}/components/txtsvc.xpt
%{_libdir}/%{name}/components/uconv.xpt
%{_libdir}/%{name}/components/unicharutil.xpt
%{_libdir}/%{name}/components/update.xpt
%{_libdir}/%{name}/components/uriloader.xpt
%{_libdir}/%{name}/components/url-classifier.xpt
%{_libdir}/%{name}/components/urlformatter.xpt
%{_libdir}/%{name}/components/webBrowser_core.xpt
%{_libdir}/%{name}/components/webapps.xpt
%{_libdir}/%{name}/components/webbrowserpersist.xpt
%{_libdir}/%{name}/components/webshell_idls.xpt
%{_libdir}/%{name}/components/widget.xpt
%{_libdir}/%{name}/components/windowds.xpt
%{_libdir}/%{name}/components/windowwatcher.xpt
%{_libdir}/%{name}/components/x*.xpt
%{_libdir}/%{name}/components/zipwriter.xpt

%{_libdir}/%{name}/components/ConsoleAPI.js
%{_libdir}/%{name}/components/ConsoleAPI.manifest
%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/FeedProcessor.manifest
%{_libdir}/%{name}/components/GPSDGeolocationProvider.js
%{_libdir}/%{name}/components/GPSDGeolocationProvider.manifest
%{_libdir}/%{name}/components/NetworkGeolocationProvider.js
%{_libdir}/%{name}/components/NetworkGeolocationProvider.manifest
%{_libdir}/%{name}/components/PlacesCategoriesStarter.js
%{_libdir}/%{name}/components/addonManager.js
%{_libdir}/%{name}/components/amContentHandler.js
%{_libdir}/%{name}/components/amWebInstallListener.js
%{_libdir}/%{name}/components/components.manifest
%{_libdir}/%{name}/components/contentAreaDropListener.js
%{_libdir}/%{name}/components/contentAreaDropListener.manifest
%{_libdir}/%{name}/components/contentSecurityPolicy.js
%{_libdir}/%{name}/components/contentSecurityPolicy.manifest
%{_libdir}/%{name}/components/crypto-SDR.js
%{_libdir}/%{name}/components/extensions.manifest
%{_libdir}/%{name}/components/interfaces.manifest
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/jsconsole-clhandler.manifest
%{_libdir}/%{name}/components/messageWakeupService.js
%{_libdir}/%{name}/components/messageWakeupService.manifest
%{_libdir}/%{name}/components/nsBadCertHandler.js
%{_libdir}/%{name}/components/nsBadCertHandler.manifest
%{_libdir}/%{name}/components/nsBlocklistService.js
%{_libdir}/%{name}/components/nsContentDispatchChooser.js
%{_libdir}/%{name}/components/nsContentDispatchChooser.manifest
%{_libdir}/%{name}/components/nsContentPrefService.js
%{_libdir}/%{name}/components/nsContentPrefService.manifest
%{_libdir}/%{name}/components/nsDefaultCLH.js
%{_libdir}/%{name}/components/nsDefaultCLH.manifest
%{_libdir}/%{name}/components/nsDownloadManagerUI.js
%{_libdir}/%{name}/components/nsDownloadManagerUI.manifest
%{_libdir}/%{name}/components/nsFilePicker.js
%{_libdir}/%{name}/components/nsFilePicker.manifest
%{_libdir}/%{name}/components/nsFormAutoComplete.js
%{_libdir}/%{name}/components/nsFormHistory.js
%{_libdir}/%{name}/components/nsHandlerService.js
%{_libdir}/%{name}/components/nsHandlerService.manifest
%{_libdir}/%{name}/components/nsHelperAppDlg.js
%{_libdir}/%{name}/components/nsHelperAppDlg.manifest
%{_libdir}/%{name}/components/nsINIProcessor.js
%{_libdir}/%{name}/components/nsINIProcessor.manifest
%{_libdir}/%{name}/components/nsInputListAutoComplete.js
%{_libdir}/%{name}/components/nsLivemarkService.js
%{_libdir}/%{name}/components/nsLoginInfo.js
%{_libdir}/%{name}/components/nsLoginManager.js
%{_libdir}/%{name}/components/nsLoginManagerPrompter.js
%{_libdir}/%{name}/components/nsMicrosummaryService.js
%{_libdir}/%{name}/components/nsPlacesAutoComplete.js
%{_libdir}/%{name}/components/nsPlacesAutoComplete.manifest
%{_libdir}/%{name}/components/nsPlacesExpiration.js
%{_libdir}/%{name}/components/nsPrompter.js
%{_libdir}/%{name}/components/nsPrompter.manifest
%{_libdir}/%{name}/components/nsProxyAutoConfig.js
%{_libdir}/%{name}/components/nsProxyAutoConfig.manifest
%{_libdir}/%{name}/components/nsSearchService.js
%{_libdir}/%{name}/components/nsSearchSuggestions.js
%{_libdir}/%{name}/components/nsTaggingService.js
%{_libdir}/%{name}/components/nsTryToClose.js
%{_libdir}/%{name}/components/nsTryToClose.manifest
%{_libdir}/%{name}/components/nsUpdateTimerManager.js
%{_libdir}/%{name}/components/nsUpdateTimerManager.manifest
%{_libdir}/%{name}/components/nsURLClassifier.manifest
%{_libdir}/%{name}/components/nsURLFormatter.js
%{_libdir}/%{name}/components/nsURLFormatter.manifest
%{_libdir}/%{name}/components/nsUrlClassifierLib.js
%{_libdir}/%{name}/components/nsUrlClassifierListManager.js
%{_libdir}/%{name}/components/nsWebHandlerApp.js
%{_libdir}/%{name}/components/nsWebHandlerApp.manifest
%{_libdir}/%{name}/components/nsXULAppInstall.js
%{_libdir}/%{name}/components/nsXULAppInstall.manifest
%{_libdir}/%{name}/components/passwordmgr.manifest
%{_libdir}/%{name}/components/pluginGlue.manifest
%{_libdir}/%{name}/components/satchel.manifest
%{_libdir}/%{name}/components/storage-Legacy.js
%{_libdir}/%{name}/components/storage-mozStorage.js
%{_libdir}/%{name}/components/toolkitplaces.manifest
%{_libdir}/%{name}/components/toolkitsearch.manifest
%{_libdir}/%{name}/components/txEXSLTRegExFunctions.js
%{_libdir}/%{name}/components/txEXSLTRegExFunctions.manifest

# do not use *.dat here, so check-files can catch any new files
# (and they won't be just silently placed empty in rpm)
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/res

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/platform.ini
%attr(755,root,root) %{_libdir}/%{name}/libmozalloc.so
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libxpcom.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%attr(755,root,root) %{_libdir}/%{name}/xpcshell
%attr(755,root,root) %{_libdir}/%{name}/xpidl
%attr(755,root,root) %{_libdir}/%{name}/xpt_dump
%attr(755,root,root) %{_libdir}/%{name}/xpt_link
%attr(755,root,root) %{_libdir}/%{name}/xulrunner-stub
%{_includedir}/%{name}
%{_datadir}/idl/%{name}
%{_libdir}/%{name}-sdk
%{_pkgconfigdir}/libxul.pc
%{_pkgconfigdir}/libxul-embedding.pc
%{_pkgconfigdir}/mozilla-js.pc
%{_pkgconfigdir}/mozilla-plugin.pc
%{_pkgconfigdir}/mozilla-gtkmozembed.pc
%{_pkgconfigdir}/mozilla-gtkmozembed-embedding.pc

%if %{without qt}
%files gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%endif
