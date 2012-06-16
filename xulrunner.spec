# TODO:
# - consider --enable-libproxy
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
# https://www.mozilla.org/security/known-vulnerabilities/firefox.html

# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)

%define		nspr_ver		4.9
%define		nss_ver			3.13.3

Summary:	XULRunner - Mozilla Runtime Environment for XUL+XPCOM applications
Summary(pl.UTF-8):	XULRunner - środowisko uruchomieniowe Mozilli dla aplikacji XUL+XPCOM
Name:		xulrunner
Version:	13.0.1
Release:	1
Epoch:		2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
# Source tarball for xulrunner is in fact firefox tarball (checked on 1.9), so lets use it
# instead of waiting for mozilla to copy file on ftp.
Source0:	http://releases.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.bz2
# Source0-md5:	82deadb501c7fc0e9fa6b025f51f05a1
Patch0:		%{name}-install.patch
Patch1:		%{name}-rpath.patch
Patch3:		%{name}-nss_cflags.patch
Patch4:		%{name}-paths.patch
Patch5:		%{name}-pc.patch
Patch6:		%{name}-prefs.patch
Patch7:		system-cairo.patch
# http://pkgs.fedoraproject.org/gitweb/?p=xulrunner.git;a=tree
Patch9:		%{name}-gtkmozembed.patch
Patch10:	%{name}-linux3.patch
Patch11:	idl-parser.patch
URL:		https://developer.mozilla.org/en/XULRunner
%{!?with_qt:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	glib2-devel >= 1:2.18
%{!?with_qt:BuildRequires:	gtk+2-devel >= 2:2.14}
BuildRequires:	hunspell-devel >= 1.2.3
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libdnet-devel
BuildRequires:	libevent-devel >= 1.4.7
# standalone libffi 3.0.9 or gcc's from 4.5(?)+
BuildRequires:	libffi-devel >= 6:3.0.9
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libiw-devel
BuildRequires:	libjpeg-devel >= 6b
%{!?with_qt:BuildRequires:	libnotify-devel >= 0.4}
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.4.1
BuildRequires:	libstdc++-devel
BuildRequires:	libvpx-devel >= 1.0.0
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	python >= 1:2.5
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.7.10
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	unzip
%if "%{pld_release}" == "ac"
BuildRequires:	xcursor-devel
BuildRequires:	xft-devel >= 2.1-2
%else
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
%endif
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
BuildConflicts:	xulrunner-devel < %{epoch}:%{name}-%{version}
Requires(post):	mktemp >= 1.5-18
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	myspell-common
Requires:	nspr >= 1:%{nspr_ver}
Requires:	nss >= 1:%{nss_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp	-D_FORTIFY_SOURCE=[0-9]+

# no Provides from private modules (don't use %{name} here, it expands to each subpackage name...)
%define		_noautoprovfiles	%{_libdir}/xulrunner/components %{_libdir}/xulrunner/plugins
# no need to require them (we have strict deps for these)
%define		_noautoreq		libmozjs.so libxpcom.so libxul.so libmozalloc.so

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
Requires:	glib2 >= 1:2.18
%{!?with_qt:Requires:	gtk+2 >= 2:2.14}
Requires:	libpng >= 1.4.1
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
Requires:	nspr-devel >= 1:%{nspr_ver}
Requires:	nss-devel >= 1:%{nss_ver}
Requires:	python-ply
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
mv -f mozilla-release mozilla
cd mozilla

# avoid using included headers (-I. is before HUNSPELL_CFLAGS)
%{__rm} extensions/spellcheck/hunspell/src/{*.hxx,hunspell.h}
# hunspell needed for factory including mozHunspell.h
echo 'LOCAL_INCLUDES += $(MOZ_HUNSPELL_CFLAGS)' >> extensions/spellcheck/src/Makefile.in

%patch0 -p2
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p2
%patch9 -p2
%patch10 -p1
%patch11 -p2

# config/rules.mk is patched by us and js/src/config/rules.mk
# is supposed to be exact copy
cp -a config/rules.mk js/src/config/rules.mk

%build
if [ "$(grep -E '^[0-9]+\.' mozilla/config/milestone.txt)" != "%{version}" ]; then
	echo >&2
	echo >&2 "Version %{version} does not match mozilla/config/milestone.txt!"
	echo >&2
	exit 1
fi

cd mozilla
cp -p %{_datadir}/automake/config.* build/autoconf

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
ac_add_options --enable-system-ffi
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
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
#mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
#ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

# files created by regxpcom
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

%{__make} -C obj-%{_target_cpu}/build/unix install \
	DESTDIR=$RPM_BUILD_ROOT

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

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/dictionaries
#%%{_libdir}/%{name}/icons

%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/components

%{_libdir}/%{name}/chrome.manifest
%{_libdir}/%{name}/omni.ja

%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container

%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%{_libdir}/%{name}/components/binary.manifest

# do not use *.dat here, so check-files can catch any new files
# (and they won't be just silently placed empty in rpm)
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
#%%{_datadir}/%{name}/icons

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
%attr(755,root,root) %{_libdir}/%{name}/xpcshell
%attr(755,root,root) %{_libdir}/%{name}/xulrunner-stub
%{_includedir}/%{name}
%{_datadir}/idl/%{name}
%dir %{_libdir}/%{name}-sdk
%{_libdir}/%{name}-sdk/bin
%{_libdir}/%{name}-sdk/idl
%{_libdir}/%{name}-sdk/lib
%{_libdir}/%{name}-sdk/include
%{_libdir}/%{name}-sdk/*.h
%dir %{_libdir}/%{name}-sdk/sdk
%{_libdir}/%{name}-sdk/sdk/lib
%dir %{_libdir}/%{name}-sdk/sdk/bin
%attr(755,root,root) %{_libdir}/%{name}-sdk/sdk/bin/*
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
