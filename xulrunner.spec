# TODO:
# - consider --enable-libproxy
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)

# On updating version, grab CVE links from:
# https://www.mozilla.org/security/known-vulnerabilities/firefox.html

# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)

%define		nspr_ver		4.9.6
%define		nss_ver			3.14.1

Summary:	XULRunner - Mozilla Runtime Environment for XUL+XPCOM applications
Summary(pl.UTF-8):	XULRunner - środowisko uruchomieniowe Mozilli dla aplikacji XUL+XPCOM
Name:		xulrunner
Version:	23.0
Release:	2
Epoch:		2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications
# Source tarball for xulrunner is in fact firefox tarball (checked on 1.9), so lets use it
# instead of waiting for mozilla to copy file on ftp.
Source0:	http://releases.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.bz2
# Source0-md5:	794e0139c4df0392146353c655d94bb9
Patch1:		%{name}-rpath.patch
Patch2:		%{name}-paths.patch
Patch3:		%{name}-pc.patch
Patch4:		%{name}-prefs.patch
Patch5:		system-cairo.patch
Patch6:		idl-parser.patch
# Edit patch below and restore --system-site-packages when system virtualenv gets 1.7 upgrade
Patch7:		system-virtualenv.patch
Patch8:		%{name}-gyp-slashism.patch
URL:		https://developer.mozilla.org/en/XULRunner
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	glib2-devel >= 1:2.20
BuildRequires:	gtk+2-devel >= 2:2.14
BuildRequires:	hunspell-devel >= 1.2.3
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libdnet-devel
BuildRequires:	libevent-devel >= 1.4.7
# standalone libffi 3.0.9 or gcc's from 4.5(?)+
BuildRequires:	libffi-devel >= 6:3.0.9
BuildRequires:	libiw-devel
# requires libjpeg-turbo implementing at least libjpeg 6b API
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libnotify-devel >= 0.4
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.5.13
BuildRequires:	libstdc++-devel
BuildRequires:	libvpx-devel >= 1.0.0
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	python >= 1:2.5
BuildRequires:	python-simplejson
BuildRequires:	python-virtualenv >= 1.9.1-4
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.7.15.2
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
BuildConflicts:	xulrunner-libs < %{epoch}:%{name}-%{version}
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
%define		_noautoreq		libmozjs.so libxul.so libmozalloc.so

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
Requires:	glib2 >= 1:2.20
Requires:	gtk+2 >= 2:2.14
Requires:	libjpeg-turbo
Requires:	libpng >= 1.5.13
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
libnotify.

%description gnome -l pl.UTF-8
Pakiet wspierający integrację XULRunnera z GNOME. Obejmuje komponenty
GConf, GIO, libnotify.

%prep
%setup -qc
mv -f mozilla-release mozilla
cd mozilla

# avoid using included headers (-I. is before HUNSPELL_CFLAGS)
%{__rm} extensions/spellcheck/hunspell/src/{*.hxx,hunspell.h}
# hunspell needed for factory including mozHunspell.h
echo 'LOCAL_INCLUDES += $(MOZ_HUNSPELL_CFLAGS)' >> extensions/spellcheck/src/Makefile.in

%patch1 -p1
%patch2 -p2
%patch3 -p1
%patch4 -p1
%patch5 -p2
%patch6 -p2
%patch7 -p2
%patch8 -p2

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
ac_add_options --disable-install-strip
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
ac_add_options --disable-crashreporter
ac_add_options --disable-elf-dynstr-gc
ac_add_options --disable-gconf
ac_add_options --disable-gnomeui
ac_add_options --disable-gnomevfs
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-long-long-warning
ac_add_options --disable-pedantic
ac_add_options --disable-updater
ac_add_options --disable-xterm-updates
ac_add_options --enable-canvas
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-extensions="default,cookie,permissions,spellcheck,gio"
ac_add_options --enable-gio
ac_add_options --enable-libxul
ac_add_options --enable-mathml
ac_add_options --enable-pango
ac_add_options --enable-readline
ac_add_options --enable-shared-js
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-ffi
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-url-classifier
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-ply
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-x
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/components \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/{lib,bin} \
	$RPM_BUILD_ROOT%{_includedir}/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/idl/%{name} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}

cd mozilla/obj-%{_target_cpu}
%{__make} -C xulrunner/installer stage-package libxul.pc libxul-embedding.pc mozilla-js.pc mozilla-plugin.pc\
	DESTDIR=$RPM_BUILD_ROOT \
	installdir=%{_libdir}/%{name} \
	INSTALL_SDK=1 \
	PKG_SKIP_STRIP=1

cp -aL xulrunner/installer/*.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -aL dist/xulrunner/* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -aL dist/include/* $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -aL dist/include/xpcom-config.h $RPM_BUILD_ROOT%{_libdir}/%{name}-devel
cp -aL dist/idl/* $RPM_BUILD_ROOT%{_datadir}/idl/%{name}
cp -aL dist/sdk/lib/* $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib
cp -aL dist/sdk/bin/* $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/bin
find $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk -name "*.pyc" | xargs rm -f

ln -s %{_libdir}/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/bin
ln -s %{_includedir}/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/include
ln -s %{_datadir}/idl/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/idl
ln -s %{_libdir}/%{name}-devel/sdk/lib $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/lib

# replace copies with symlinks
ln -sf %{_libdir}/%{name}/libmozjs.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libmozjs.so
ln -sf %{_libdir}/%{name}/libxul.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libxul.so
ln -sf %{_libdir}/%{name}/libmozalloc.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libmozalloc.so
# temp fix for https://bugzilla.mozilla.org/show_bug.cgi?id=63955
chmod a+rx $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/bin/xpt.py

ln -sf %{_libdir}/%{name}/xulrunner $RPM_BUILD_ROOT%{_bindir}/xulrunner

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

# files created by regxpcom
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

# Install xpcshell and run-mozilla.sh
%{__cp} -pL dist/bin/xpcshell $RPM_BUILD_ROOT%{_libdir}/%{name}
%{__cp} -pL dist/bin/run-mozilla.sh $RPM_BUILD_ROOT%{_libdir}/%{name}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

# remove unecessary stuff
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/LICENSE

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
%attr(755,root,root) %{_libdir}/%{name}/xulrunner

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/dictionaries

%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/components

%{_libdir}/%{name}/chrome.manifest

%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container

%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%{_libdir}/%{name}/components/components.manifest

# do not use *.dat here, so check-files can catch any new files
# (and they won't be just silently placed empty in rpm)
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/platform.ini
%attr(755,root,root) %{_libdir}/%{name}/libmozalloc.so
%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/omni.ja

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/xpcshell
%attr(755,root,root) %{_libdir}/%{name}/xulrunner-stub
%{_includedir}/%{name}
%{_datadir}/idl/%{name}
%dir %{_libdir}/%{name}-devel
%{_libdir}/%{name}-devel/bin
%{_libdir}/%{name}-devel/idl
%{_libdir}/%{name}-devel/lib
%{_libdir}/%{name}-devel/include
%{_libdir}/%{name}-devel/*.h
%dir %{_libdir}/%{name}-devel/sdk
%{_libdir}/%{name}-devel/sdk/lib
%dir %{_libdir}/%{name}-devel/sdk/bin
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/*
%{_pkgconfigdir}/libxul.pc
%{_pkgconfigdir}/libxul-embedding.pc
%{_pkgconfigdir}/mozilla-js.pc
%{_pkgconfigdir}/mozilla-plugin.pc

%files gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
