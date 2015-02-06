%define major 0
%define libname %mklibname bt %major
# fwang: we don't use libbt-devel because it is already occupied by libbt
%define develname %mklibname -d blackbox

Summary:  	A Window Manager for the X Window System
Name:		blackbox
Version:	0.70.1
Release:	17
License:	BSD-like
Group:		Graphical desktop/Other
URL:		http://blackboxwm.sourceforge.net/
Source0:	blackbox-%{version}.tar.bz2
Source1:	blackbox.xdg
Source3:	blackbox.png
Source4:	blackbox32.png
Source5:	blackbox-startblackbox
Patch0:		blackbox-0.70.1-gcc43.patch
Patch1:		blackbox-0.70.1-x11-1.4.patch
Requires:	desktop-common-data
Requires:	xdg-compliance-menu
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xft)
BuildRequires:  locales-en
Requires:	%libname = %version-%release

%description
This is a window manager for X.  It is similar in many respects to
such popular packages as Window Maker, Enlightenment, and FVWM2.  You
might be interested in this package if you are tired of window managers
that are a heavy drain on your system resources, but you still want
an attractive and modern-looking interface.
.
The best part of all is that this program is coded in C++, so it
is even more attractive "under the hood" than it is in service -- no
small feat.
.
If none of this sounds familiar to you, or you want your computer to
look like Windows 98, you probably don't want this package.

%package -n %libname
Group:		Graphical desktop/Other
Summary:	Library files for blackbox

%description -n %libname
This package contains library fiiles needed for blackbox.

%package -n %develname
Group:		Development/X11
Summary:	Developemnt files provided by blackbox
Provides:	%{name}-devel = %version-%release
Requires:	%libname = %version-%release
Conflicts:	%name < 0.70.1-6

%description -n %develname
This package contains developemnt files provided by blackbox.

%prep
%setup -q
%patch0 -p1 -b .gcc43
%patch1 -p0

%build
export LANG="en_US" LC_ALL="en_US"
%configure2_5x --enable-kde --enable-nls --enable-shared --disable-static

%make DEFAULT_MENU=%{_sysconfdir}/menu.d/%name

%install
mkdir -p %{buildroot}%{_prefix}
%makeinstall_std

#mkdir -p %{buildroot}%{_prefix}/bin
#install -m755 %{buildroot}%{_bindir}/* %{buildroot}%{_prefix}/bin/
# and removing the files from _bindir if they are not packaged; otherwise
# the rpm checking makes the building of the package fail -- pablo
#rm -f %{buildroot}%{_bindir}/*

install -m755 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/menu.d/%{name}

mkdir -p %{buildroot}%_sysconfdir/X11/%{name}
touch %{buildroot}%_sysconfdir/X11/%{name}/%{name}-menu

install -m644 %{SOURCE3} -D %{buildroot}%{_miconsdir}/blackbox.png
install -m644 %{SOURCE4} -D %{buildroot}%{_iconsdir}/blackbox.png

# bsetroot is an alternative for the one in fluxbox
mv %{buildroot}%{_bindir}/bsetroot %{buildroot}%{_bindir}/bsetroot-blackbox


rm -f %{buildroot}/%{_libdir}/*.a \
        %{buildroot}/%{_libdir}/*.la

mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat > %{buildroot}/%{_sysconfdir}/X11/wmsession.d/05blackbox << EOF
NAME=BlackBox
ICON=blackbox.png
EXEC=%{_bindir}/blackbox
DESC=A Light but nice looking window manager
SCRIPT:
exec %{_bindir}/startblackbox
EOF

install -m 755 %{SOURCE5} %{buildroot}/usr/bin/startblackbox

%post
%{update_desktop_database}
%{make_session}

#blackbox-alternatives
update-alternatives --install %{_bindir}/bsetroot bsetroot %{_bindir}/bsetroot-%name 10

%postun
%{clean_desktop_database}

# Remove bsetroot-alternatives
if [ "$1" = 0 ]; then
update-alternatives --remove bsetroot %{_bindir}/bsetroot-%name
fi

%files
%config(noreplace) %{_sysconfdir}/menu.d/%{name}
%config(noreplace) %{_sysconfdir}/X11/%{name}/%{name}-menu
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/05blackbox
%{_bindir}/*
%{_datadir}/blackbox
%{_iconsdir}/blackbox.png
%{_miconsdir}/blackbox.png
%{_mandir}/man1/*

%files -n %libname
%_libdir/*.so.%{major}*

%files -n %develname
%_libdir/*.so
%_includedir/bt
%{_libdir}/pkgconfig/libbt.pc
