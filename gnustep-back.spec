Summary:	The GNUstep backend bundle
Summary(pl):	Pakiet backendowy GNUstep
Name:		gnustep-back
Version:	0.8.3
Release:	1
License:	LGPL/GPL
Vendor:		The GNUstep Project
Group:		X11/Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
Patch0:		%{name}-Xft2.patch
Patch1:		%{name}-art-freetype213.patch
Patch2:		%{name}-xdps-fix.patch
URL:		http://www.gnustep.org/
BuildRequires:	OpenGL-devel
BuildRequires:	WindowMaker-devel
BuildRequires:	XFree86-devel
BuildRequires:	XFree86-DPS-devel
BuildRequires:	Xft-devel
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	gnustep-gui-devel
BuildRequires:	libart_lgpl-devel
Requires:	OpenGL
Requires:	gnustep-gui
Obsoletes:	gnustep-xgps
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/lib/GNUstep

%define		libcombo	gnu-gnu-gnu
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%{_target_cpu}
%endif

%description
This is a backend for the GNUstep gui Library which allows you to use
the GNUstep gui Library on an X Windows System (other backends will
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
Requires:	%{name} = %{version}
Conflicts:	gnustep-core

%description art
GNUstep graphics backend - art.

%description art -l pl
Graficzny backend GNUstep - art.

%package xdps
Summary:	GNUstep graphics backend - xdps
Summary(pl):	Graficzny backend GNUstep - xdps
Group:		X11/Libraries
Requires:	%{name} = %{version}
Obsoletes:	gnustep-xdps
Conflicts:	gnustep-core

%description xdps
GNUstep graphics backend - xdps.

%description xdps -l pl
Graficzny backend GNUstep - xdps.

%package devel
Summary:	Headers for GNUstep backends
Summary(pl):	Pliki nag³ówkowe backendów GNUstep
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Requires:	XFree86-devel
Requires:	Xft-devel
Requires:	gnustep-gui-devel
Obsoletes:	gnustep-xdps-devel
Obsoletes:	gnustep-xgps-devel
Conflicts:	gnustep-core

%description devel
This package contains development headers for GNUstep backends. It
includes also files specific for all x11 graphic backends (xlib,
art, xdps).

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe dla backendów GNUstep, w tym pliki
specyficzne dla wszystkich backendów graficznych dla x11 (xlib, art,
xdps).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
. %{_prefix}/System/Makefiles/GNUstep.sh
for g in art xdps xlib ; do
if [ "$g" = "xlib" ]; then
	INC='--with-include-flags=-I/usr/include/freetype2'
	NAME="back"
else
	INC=
	NAME="back-$g"
fi
%configure \
	--enable-graphics=$g \
	--with-name=$NAME \
	$INC

%{__make} \
	messages=yes
cp -f back.make back-$g.make
done

%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
. %{_prefix}/System/Makefiles/GNUstep.sh

for g in art xdps xlib ; do
if [ "$g" = "xlib" ]; then
	NAME="back"
else
	NAME="back-$g"
fi
%{__make} install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System \
	BUILD_GRAPHICS="$g" \
	BACKEND_NAME="$NAME"
done

%{__make} install -C Documentation \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System \
# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_prefix}/System/Documentation -type f | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%{_prefix}/System/Documentation/Developer/Back

%dir %{_prefix}/System/Library/Bundles/libgnustep-back.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back.bundle/%{gscpu}

%attr(755,root,root) %{_prefix}/System/Tools/%{gscpu}/%{gsos}/%{libcombo}/*

%files art
%defattr(644,root,root,755)
%dir %{_prefix}/System/Library/Bundles/libgnustep-back-art.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back-art.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back-art.bundle/%{gscpu}

%files xdps
%defattr(644,root,root,755)
%dir %{_prefix}/System/Library/Bundles/libgnustep-back-xdps.bundle
%{_prefix}/System/Library/Bundles/libgnustep-back-xdps.bundle/Resources
%attr(755,root,root) %{_prefix}/System/Library/Bundles/libgnustep-back-xdps.bundle/%{gscpu}

%files devel
%defattr(644,root,root,755)
%{_prefix}/System/Headers/gnustep/gsc
%{_prefix}/System/Headers/gnustep/x11

%{_prefix}/System/Headers/gnustep/xlib
%{_prefix}/System/Headers/gnustep/art
%{_prefix}/System/Headers/gnustep/xdps
