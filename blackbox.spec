%define major 0
%define libname %mklibname bt %major
# fwang: we don't use libbt-devel because it is already occupied by libbt
%define develname %mklibname -d blackbox

Summary:  	A Window Manager for the X Window System
Name:		blackbox
Version:	0.70.1
Release:	%mkrel 12
License:	BSD-like
Group:		Graphical desktop/Other
URL:		http://blackboxwm.sourceforge.net/
Source:		blackbox-%{version}.tar.bz2
Source1:	blackbox.xdg
Source3:	blackbox.png
Source4:	blackbox32.png
Source5:	blackbox-startblackbox
Patch0:		blackbox-0.70.1-gcc43.patch
Requires:	desktop-common-data
BuildRequires:	X11-devel 
BuildRequires:  locales-en
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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

%build
export LANG="en_US" LC_ALL="en_US"
%configure2_5x --enable-kde --enable-nls --enable-shared --disable-static

%if %mdkversion >= 200700
%make DEFAULT_MENU=%{_sysconfdir}/menu.d/%name
%else
%make DEFAULT_MENU=%{_sysconfdir}/X11/blackbox/blackbox-menu
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}
%makeinstall

#mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
#install -m755 $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_prefix}/bin/
# and removing the files from _bindir if they are not packaged; otherwise
# the rpm checking makes the building of the package fail -- pablo
#rm -f $RPM_BUILD_ROOT%{_bindir}/*

install -m755 %{SOURCE1} -D $RPM_BUILD_ROOT%{_sysconfdir}/menu.d/%{name}

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/X11/%{name}
touch $RPM_BUILD_ROOT%_sysconfdir/X11/%{name}/%{name}-menu

install -m644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_miconsdir}/blackbox.png
install -m644 %{SOURCE4} -D $RPM_BUILD_ROOT%{_iconsdir}/blackbox.png

# bsetroot is an alternative for the one in fluxbox
mv $RPM_BUILD_ROOT%{_bindir}/bsetroot $RPM_BUILD_ROOT%{_bindir}/bsetroot-blackbox


rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a \
        $RPM_BUILD_ROOT/%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d
cat > $RPM_BUILD_ROOT/%{_sysconfdir}/X11/wmsession.d/05blackbox << EOF
NAME=BlackBox
ICON=blackbox.png
EXEC=%{_bindir}/blackbox
DESC=A Light but nice looking window manager
SCRIPT:
exec %{_bindir}/startblackbox
EOF

install -m 755 %{SOURCE5} $RPM_BUILD_ROOT/usr/bin/startblackbox


%find_lang %{name}

%post
%{update_desktop_database}
%{make_session}

#blackbox-alternatives
update-alternatives --install %{_bindir}/bsetroot bsetroot %{_bindir}/bsetroot-%name 10

%postun
%{clean_desktop_database}
%{make_session}

# Remove bsetroot-alternatives
if [ "$1" = 0 ]; then
update-alternatives --remove bsetroot %{_bindir}/bsetroot-%name
fi

%clean
rm -fr $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root) 
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
