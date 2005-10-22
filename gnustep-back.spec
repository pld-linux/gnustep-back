# TODO:
# - symlink Helvetica from ghostscript-fonts-std?
#
# Conditional build:
%bcond_without	art	# don't build art backend
%bcond_without	cairo	# don't build cairo backend
#
Summary:	The GNUstep backend bundle
Summary(pl):	Pakiet backendowy GNUstep
Name:		gnustep-back
Version:	0.10.1
Release:	1
License:	LGPL/GPL
Vendor:		The GNUstep Project
Group:		X11/Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	139052b97ca5111dbcc9dd6b83c8d66f
URL:		http://www.gnustep.org/
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	XFree86-DPS-devel
%{?with_cairo:BuildRequires:	cairo-devel >= 1.0}
%{?with_art:BuildRequires:	freetype-devel >= 2.1.8}
BuildRequires:	gnustep-gui-devel >= %{version}
%{?with_art:BuildRequires:	libart_lgpl-devel}
BuildRequires:	pkgconfig
BuildRequires:	xft-devel
Requires:	OpenGL
Requires:	gnustep-gui >= %{version}
Obsoletes:	gnustep-back-devel
Obsoletes:	gnustep-xgps
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/%{_lib}/GNUstep

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%define		libcombo	gnu-gnu-gnu
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%(echo %{_target_cpu} | sed -e 's/amd64/x86_64/;s/ppc/powerpc/')
%endif

%description
This is a backend for the GNUstep gui Library which allows you to use
the GNUstep gui Library on an X Window System (other backends will
be added later to allow you to use the GNUstep gui Library in other
windowing environments).

This package contains common part and xlib graphics backend.

%description -l pl
To jest backend dla biblioteki GNUstep GUI, pozwalaj±cy na u¿ywanie
biblioteki graficznego interfejsu u¿ytkownika GNUstep pod systemem X
Window (inne backendy, pozwalaj±ce na u¿ywanie biblioteki GNUstep GUI
w innych ¶rodowiskach okienkowych, zostan± dodane pó¼niej).

Ten pakiet zawiera czê¶æ wspóln± i backend graficzny xlib.

%package art
Summary:	GNUstep graphics backend - art
Summary(pl):	Graficzny backend GNUstep - art
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype >= 2.1.8
Conflicts:	gnustep-core

%description art
GNUstep graphics backend - art.

%description art -l pl
Graficzny backend GNUstep - art.

%package cairo
Summary:	GNUstep graphics backend - cairo
Summary(pl):	Graficzny backend GNUstep - cairo
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo >= 1.0

%description cairo
GNUstep graphics backend - cairo.

%description cairo -l pl
Graficzny backend GNUstep - cairo.

%package xdps
Summary:	GNUstep graphics backend - xdps
Summary(pl):	Graficzny backend GNUstep - xdps
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	gnustep-xdps
Conflicts:	gnustep-core

%description xdps
GNUstep graphics backend - xdps.

%description xdps -l pl
Graficzny backend GNUstep - xdps.

%prep
%setup -q

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
install -d back-xdps
cp -a `cat files.list` back-xdps
ln -sf . back-xlib

%build
. %{_prefix}/System/Library/Makefiles/GNUstep.sh

for g in %{?with_art:art} %{?with_cairo:cairo} xdps xlib ; do
cd back-$g
if [ "$g" = "xlib" ]; then
	NAME="back"
else
	NAME="back-$g"
fi
if [ "$g" = "cairo" ]; then
	CPPFLAGS="-I/usr/include/freetype2"
fi
%configure \
	--enable-graphics=$g \
	--with-name=$NAME

%{__make} \
	messages=yes
cd ..
done

%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
. %{_prefix}/System/Library/Makefiles/GNUstep.sh

for g in %{?with_art:art} %{?with_cairo:cairo} xdps xlib ; do
if [ "$g" = "xlib" ]; then
	NAME="back"
else
	NAME="back-$g"
fi
%{__make} install -C back-$g \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System \
	BUILD_GRAPHICS="$g" \
	BACKEND_NAME="$NAME"
done

%{__make} install -C Documentation \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System \

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation -type f \
	! -name '*.gz' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%docdir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Documentation/Developer/Back
%{_prefix}/System/Library/Documentation/man/man1/gpbs.1*

%dir %{_prefix}/System/Library/Bundles/libgnustep-back-010.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back-010.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back-010.bundle/%{gscpu}

# XXX: n0190{0,2,4,6}{3,4}.{pfb,afm,pfm} - symlink from ghostscript-fonts-std?
%{_prefix}/System/Library/Fonts/Helvetica.nfont

%attr(755,root,root) %{_prefix}/System/Tools/%{gscpu}/%{gsos}/%{libcombo}/*

%if %{with art}
%files art
%defattr(644,root,root,755)
%dir %{_prefix}/System/Library/Bundles/libgnustep-back-art-010.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back-art-010.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back-art-010.bundle/%{gscpu}
%endif

%if %{with cairo}
%files cairo
%defattr(644,root,root,755)
%dir %{_prefix}/System/Library/Bundles/libgnustep-back-cairo-010.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back-cairo-010.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back-cairo-010.bundle/%{gscpu}
%endif

%files xdps
%defattr(644,root,root,755)
%dir %{_prefix}/System/Library/Bundles/libgnustep-back-xdps-010.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back-xdps-010.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back-xdps-010.bundle/%{gscpu}
