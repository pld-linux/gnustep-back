# TODO:
# - symlink Helvetica from ghostscript-fonts-std?
#
# Conditional build:
%bcond_without	art	# art backend
%bcond_with	dps	# xdps backend
%bcond_without	cairo	# cairo backend
%bcond_with	glitz	# glitz support in cairo backend (requires cairo built with glitz)
#
Summary:	The GNUstep backend bundle
Summary(pl.UTF-8):	Pakiet backendowy GNUstep
Name:		gnustep-back
Version:	0.24.0
Release:	1
License:	LGPL v2+ (libraries), GPL v3+ (applicatinos)
Vendor:		The GNUstep Project
Group:		X11/Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	0b8393832bd928b9d3ec4eb68d7f6564
Patch0:		%{name}-format.patch
URL:		http://www.gnustep.org/
BuildRequires:	OpenGL-GLX-devel
%{?with_dps:BuildRequires:	X11-DPS-devel}
%{?with_cairo:BuildRequires:	cairo-devel >= 1.0}
%{?with_cairo:BuildRequires:	fontconfig-devel}
%{?with_art:BuildRequires:	freetype-devel >= 1:2.1.8}
%{?with_glitz:BuildRequires:	glitz-devel}
BuildRequires:	gnustep-gui-devel >= %{version}
%{?with_art:BuildRequires:	libart_lgpl-devel}
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXmu-devel
%{?with_cairo:BuildRequires:	xorg-lib-libXrender-devel}
%{?with_dps:BuildRequires:	xorg-lib-libXt-devel}
Requires:	gnustep-gui >= %{version}
Obsoletes:	gnustep-back-devel
%{!?with_dps:Obsoletes:	gnustep-back-xdps}
Obsoletes:	gnustep-xgps
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# bundles version (echo %{version} | cut -d. -f1,2 | tr -d .)
%define		bver	024

%description
This is a backend for the GNUstep gui Library which allows you to use
the GNUstep gui Library on an X Window System (other backends will
be added later to allow you to use the GNUstep gui Library in other
windowing environments).

This package contains common part and xlib graphics backend.

%description -l pl.UTF-8
To jest backend dla biblioteki GNUstep GUI, pozwalający na używanie
biblioteki graficznego interfejsu użytkownika GNUstep pod systemem X
Window (inne backendy, pozwalające na używanie biblioteki GNUstep GUI
w innych środowiskach okienkowych, zostaną dodane później).

Ten pakiet zawiera część wspólną i backend graficzny xlib.

%package art
Summary:	GNUstep graphics backend - art
Summary(pl.UTF-8):	Graficzny backend GNUstep - art
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype >= 1:2.1.8
Conflicts:	gnustep-core

%description art
GNUstep graphics backend - art.

%description art -l pl.UTF-8
Graficzny backend GNUstep - art.

%package cairo
Summary:	GNUstep graphics backend - cairo
Summary(pl.UTF-8):	Graficzny backend GNUstep - cairo
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo >= 1.0

%description cairo
GNUstep graphics backend - cairo.

%description cairo -l pl.UTF-8
Graficzny backend GNUstep - cairo.

%package xdps
Summary:	GNUstep graphics backend - xdps
Summary(pl.UTF-8):	Graficzny backend GNUstep - xdps
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	gnustep-xdps
Conflicts:	gnustep-core

%description xdps
GNUstep graphics backend - xdps.

%description xdps -l pl.UTF-8
Graficzny backend GNUstep - xdps.

%prep
%setup -q
%patch -P0 -p1

%if %{with cairo}
# hack cairo header - objc doesn't allow #defines in #include
sed -e 's,FT_FREETYPE_H,<freetype/freetype.h>,' /usr/include/cairo/cairo-ft.h > \
	Headers/cairo-ft.h
%endif

# prepare the trees (for art, cairo, xdps, xlib backends)
echo * > files.list
%if %{with art}
install -d back-art 
cp -a `cat files.list` back-art
%endif
%if %{with cairo}
install -d back-cairo
cp -a `cat files.list` back-cairo
%endif
%if %{with dps}
install -d back-xdps
cp -a `cat files.list` back-xdps
%endif
ln -sf . back-xlib

%build
export GNUSTEP_MAKEFILES=%{_datadir}/GNUstep/Makefiles
export GNUSTEP_FLATTENED=yes
export GNUSTEP_INSTALLATION_DOMAIN=SYSTEM

for g in %{?with_art:art} %{?with_cairo:cairo} %{?with_dps:xdps} xlib ; do
cd back-$g
if [ "$g" = "xlib" ]; then
	NAME="back"
else
	NAME="back-$g"
fi
if [ "$g" = "cairo" ]; then
	CPPFLAGS="%{rpmcppflags} -I/usr/include/freetype2"
fi
%configure \
	%{!?with_glitz:--disable-glitz} \
	--enable-graphics=$g \
	--with-name=$NAME

%{__make} \
	messages=yes
cd ..
done

%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
export GNUSTEP_MAKEFILES=%{_datadir}/GNUstep/Makefiles
export GNUSTEP_FLATTENED=yes
export GNUSTEP_INSTALLATION_DOMAIN=SYSTEM

for g in %{?with_art:art} %{?with_cairo:cairo} %{?with_dps:xdps} xlib ; do
if [ "$g" = "xlib" ]; then
	NAME="back"
else
	NAME="back-$g"
fi
%{__make} install -C back-$g \
	DESTDIR=$RPM_BUILD_ROOT \
	BUILD_GRAPHICS="$g" \
	BACKEND_NAME="$NAME"
done

%{__make} install -C Documentation \
	DESTDIR=$RPM_BUILD_ROOT

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_datadir}/GNUstep/Documentation \
	-type f -a ! -name '*.html' -a ! -name '*.gz' -a ! -name '*.jpg' -a ! -name '*.css' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog

%docdir %{_datadir}/GNUstep/Documentation
%{_datadir}/GNUstep/Documentation/Developer/Back

%attr(755,root,root) %{_bindir}/font_cacher
%attr(755,root,root) %{_bindir}/gpbs

%{_mandir}/man1/gpbs.1*

%dir %{_libdir}/GNUstep/Bundles/libgnustep-back-%{bver}.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/libgnustep-back-%{bver}.bundle/libgnustep-back-%{bver}
%{_libdir}/GNUstep/Bundles/libgnustep-back-%{bver}.bundle/Resources
%{_libdir}/GNUstep/Bundles/libgnustep-back-%{bver}.bundle/stamp.make

%dir %{_libdir}/GNUstep/Fonts
# XXX: n0190{0,2,4,6}{3,4}.{pfb,afm,pfm} - symlink from ghostscript-fonts-std?
%{_libdir}/GNUstep/Fonts/Helvetica.nfont

%if %{with art}
%files art
%defattr(644,root,root,755)
%dir %{_libdir}/GNUstep/Bundles/libgnustep-back-art-%{bver}.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/libgnustep-back-art-%{bver}.bundle/libgnustep-back-art-%{bver}
%{_libdir}/GNUstep/Bundles/libgnustep-back-art-%{bver}.bundle/Resources
%{_libdir}/GNUstep/Bundles/libgnustep-back-art-%{bver}.bundle/stamp.make
%endif

%if %{with cairo}
%files cairo
%defattr(644,root,root,755)
%dir %{_libdir}/GNUstep/Bundles/libgnustep-back-cairo-%{bver}.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/libgnustep-back-cairo-%{bver}.bundle/libgnustep-back-cairo-%{bver}
%{_libdir}/GNUstep/Bundles/libgnustep-back-cairo-%{bver}.bundle/Resources
%{_libdir}/GNUstep/Bundles/libgnustep-back-cairo-%{bver}.bundle/stamp.make
%endif

%if %{with dps}
%files xdps
%defattr(644,root,root,755)
%dir %{_libdir}/GNUstep/Bundles/libgnustep-back-xdps-%{bver}.bundle
%attr(755,root,root) %{_libdir}/GNUstep/Bundles/libgnustep-back-xdps-%{bver}.bundle/libgnustep-back-xdps-%{bver}
%{_libdir}/GNUstep/Bundles/libgnustep-back-xdps-%{bver}.bundle/Resources
%{_libdir}/GNUstep/Bundles/libgnustep-back-xdps-%{bver}.bundle/stamp.make
%endif
