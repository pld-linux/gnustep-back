Summary:	The GNUstep backend bundle
Summary(pl):	Pakiet backendowy GNUstep
Name:		gnustep-back
Version:	0.8.9
Release:	1
License:	LGPL/GPL
Vendor:		The GNUstep Project
Group:		X11/Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz
# Source0-md5:	af2ba9a683a28f75ebdeb91dd58debec
Patch0:               %{name}-xdps-fix.patch
URL:		http://www.gnustep.org/
BuildRequires:	OpenGL-devel
BuildRequires:	WindowMaker-devel
BuildRequires:	XFree86-devel
BuildRequires:	XFree86-DPS-devel
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	gnustep-gui-devel >= %{version}
BuildRequires:	libart_lgpl-devel
BuildRequires:	xft-devel
Requires:	OpenGL
Requires:	gnustep-gui >= %{version}
Obsoletes:	gnustep-back-devel
Obsoletes:	gnustep-xgps
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/lib/GNUstep

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

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
Requires:	%{name} = %{version}
Requires:	freetype >= 2.1.4
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

%prep
%setup -q
%patch0 -p1

# prepare three trees (for art, xdps and xlib backends)
echo * > files.list
install -d back-art back-xdps
cp -a `cat files.list` back-art
cp -a `cat files.list` back-xdps
ln -sf . back-xlib

%build
. %{_prefix}/System/Library/Makefiles/GNUstep.sh

for g in art xdps xlib ; do
cd back-$g
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
cd ..
done

%{__make} -C Documentation

%install
rm -rf $RPM_BUILD_ROOT
. %{_prefix}/System/Library/Makefiles/GNUstep.sh

for g in art xdps xlib ; do
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
