%define name freetennis
%define version 0.4.8
%define release %mkrel 1

Summary: A free tennis simulation
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://heanet.dl.sourceforge.net/sourceforge/freetennis/%{name}-%{version}.tar.bz2
#Patch0: freetennis-0.1-version.patch.bz2
License: GPL
Group: Games/Sports
Url: http://freetennis.sourceforge.net/
BuildRequires: ocaml-lablgl
BuildRequires: ocaml-lablgl-devel
BuildRequires: ocaml-SDL-devel
BuildRequires: ocaml-camlimages-devel
Buildrequires: ocaml-lablgtk2-devel

%description
Free Tennis is a tennis simulation developed by a former tennis
player. Its main feature is realism. For gameplay, this means you have
total control over the shot parabola. For graphics, it means players
have realistic gestures. For AI, it means real tactics.

%prep
%setup -q
#patch0 -p1 -b .version

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_bindir
mkdir -p $RPM_BUILD_ROOT%_libdir/%name
tar c freetennis graphics sfx | tar x -C $RPM_BUILD_ROOT%_libdir/%name

cat > $RPM_BUILD_ROOT%_bindir/%name <<EOF
#!/bin/sh
cd %_libdir/%name
exec soundwrapper ./freetennis "\$@"
EOF

chmod 0755 $RPM_BUILD_ROOT%_bindir/%name

# install menu entry
install -d %buildroot/%_menudir
cat <<EOF > %buildroot/%_menudir/%name
?package(%name): needs=X11 \
section="More Applications/Games/Sports" \
title="Free Tennis" \
longtitle="Tennis game" \
command="freetennis -realistic" \
icon="sport_section.png"
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc web-site/manual.html AUTHORS
%_bindir/*
%_libdir/%name
%_menudir/%name

