# Empty file debugsourcefiles.list
%global debug_package %{nil}

%global majorversion 4.20
%global patchlevel 0
%global upstreamversion %{majorversion}.%{patchlevel}

#%%global rcrel -rc5

%bcond tests 0
%bcond stage2 0

Name:           lean4
# minor point releases provide the same version
Version:        %{majorversion}.0
Release:        1%{?rcrel}%{?dist}
Summary:        Functional programming language and theorem prover

License:        Apache-2.0
URL:            https://lean-lang.org/
Source0:        https://github.com/leanprover/lean4/archive/refs/tags/v%{upstreamversion}%{?rcrel}.tar.gz#/%{name}-%{upstreamversion}%{?rcrel}.tar.gz
%if %{defined fedora}
BuildRequires:  cadical
%else
# also needed to build mimalloc from source
BuildRequires:  git-core
%endif
%if %{with stage2}
BuildRequires:  ccache
%endif
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  libuv-devel
#BuildRequires:  mimalloc-devel
ExcludeArch:    s390x %{ix86}
Provides:       %{name}-static = %{version}-%{release}

%description
Lean is a functional programming language that makes it easy to write
correct and maintainable code. You can also use Lean as an interactive
theorem prover. Lean programming primarily involves defining types and
functions. This allows your focus to remain on the problem domain and
manipulating its data, rather than the details of programming.


%prep
%setup -q -n %{name}-%{upstreamversion}%{?rcrel}


%build
%cmake \
  -DLEAN_BUILD_TYPE="RELEASE" \
  -DUSE_GITHASH=OFF \
  -DLEAN_INSTALL_PREFIX=%{buildroot} \
  -DINSTALL_CADICAL=OFF \
  -DUSE_MIMALLOC=OFF
%cmake_build
%if %{with stage2}
# failing
make -C redhat-linux-build stage2
%endif


%install
# cmake_install does not do anything
%if %{with stage2}
make -C redhat-linux-build/stage2 install
%else
make -C redhat-linux-build/stage1 install
%endif

%define lean lean4
%global leandir %{_libdir}/%{lean}
mkdir -p %{buildroot}%{_libdir}
rm -f %{buildroot}/lean-%{version}-linux/LICENSE*
mv %{buildroot}/lean-%{version}-linux %{buildroot}%{leandir}

strip %{buildroot}%{leandir}/bin/{lake,lean,leanc}
chmod a+x %{buildroot}%{leandir}/lib/lean/lib*shared.so
strip %{buildroot}%{leandir}/lib/lean/lib*shared.so

mkdir -p %{buildroot}%{_bindir}
(
cd %{buildroot}%{_bindir}
ln -s ../%{_lib}/%{lean}/bin/* .
)


%check
%if %{with tests}
%ctest
%endif


%files
%license LICENSE
%doc CONTRIBUTING.md README.md RELEASES.md
%{_bindir}/lake
%{_bindir}/lean
%{_bindir}/leanc
%{_bindir}/leanmake
%dir %{leandir}
%{leandir}/bin
%dir %{leandir}/include
%{leandir}/include/lean
%dir %{leandir}/lib
%{leandir}/lib/lean
%dir %{leandir}/share
%{leandir}/share/lean
%dir %{leandir}/src
%{leandir}/src/lean


%changelog
* Tue Jun 03 2025 Jens Petersen <petersen@redhat.com> - 4.20.0-1
- https://lean-lang.org/doc/reference/latest/releases/v4.20.0/#release-v4___20___0

* Sat May 03 2025 Jens Petersen <petersen@redhat.com> - 4.19.0-1
- https://lean-lang.org/doc/reference/latest/releases/v4.19.0/#release-v4___19___0

* Wed Apr 02 2025 Jens Petersen <petersen@redhat.com> - 4.18.0-1
- https://lean-lang.org/doc/reference/latest/releases/v4.18.0/#release-v4___18___0

* Wed Mar 05 2025 Jens Petersen <petersen@redhat.com> - 4.17.0-1
- https://lean-lang.org/doc/reference/latest/releases/v4.17.0/#release-v4___17___0

* Mon Feb  3 2025 Jens Petersen <petersen@redhat.com> - 4.16.0-1
- https://lean-lang.org/doc/reference/latest/releases/v4.16.0/#release-v4___16___0

* Wed Jan  8 2025 Jens Petersen <petersen@redhat.com> - 4.15.0-1
- https://lean-lang.org/doc/reference/latest/releases/v4.15.0/#release-v4___15___0

* Mon Dec  2 2024 Jens Petersen <petersen@redhat.com> - 4.14.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.14.0
- https://lean-lang.org/blog/2024-12-9-lean-4140/

* Sat Nov 23 2024 Jens Petersen <petersen@redhat.com> - 4.13.0-4
- use sed to override GMP_LIBRARIES and LIBUV_LIBRARIES with pkgconf --libs

* Fri Nov 22 2024 Jens Petersen <petersen@redhat.com> - 4.13.0-3
- override cmake LIBUV_LIBRARIES with pkgconf --libs

* Sun Nov  3 2024 Jens Petersen <petersen@redhat.com> - 4.13.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.13.0

* Sun Nov  3 2024 Jens Petersen <petersen@redhat.com> - 4.12.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.12.0

* Thu Oct  3 2024 Jens Petersen <petersen@redhat.com> - 4.11.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.11.0

* Thu Aug  1 2024 Jens Petersen <petersen@redhat.com> - 4.10.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.10.0
- add some macros to handle minor point releases

* Fri Jul 12 2024 Jens Petersen <petersen@redhat.com> - 4.9.0-2
- https://github.com/leanprover/lean4/releases/tag/v4.9.1

* Wed Jul  3 2024 Jens Petersen <petersen@redhat.com> - 4.9.0-1
- https://lean-lang.org/blog/2024-7-1-lean-490/
- https://github.com/leanprover/lean4/releases/tag/v4.9.0

* Thu Jun  6 2024 Jens Petersen <petersen@redhat.com> - 4.8.0-1
- https://lean-lang.org/blog/2024-6-1-lean-480/
- https://github.com/leanprover/lean4/releases/tag/v4.8.0

* Fri May 17 2024 Jens Petersen <petersen@redhat.com> - 4.7.0-4
- link with -lgmp instead of libgmp.so file

* Thu May  2 2024 Jens Petersen <petersen@redhat.com> - 4.7.0-3
- install under libdir/lean4 for now with symlinks to bindir

* Tue Apr 30 2024 Jens Petersen <petersen@redhat.com> - 4.7.0-2
- strip bin and lib*.so files

* Mon Apr 29 2024 Jens Petersen <petersen@redhat.com> - 4.7.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.7.0
- https://lean-lang.org/blog/2024-4-4-lean-470/

* Tue Dec 12 2023 Jens Petersen <petersen@redhat.com> - 4.3.0.-1
- initial packaging
