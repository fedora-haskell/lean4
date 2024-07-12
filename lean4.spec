# Empty file debugsourcefiles.list
%global debug_package %{nil}

Name:           lean4
Version:        4.9.1
Release:        1%{?dist}
Summary:        Functional programming language and theorem prover

License:        Apache-2.0
URL:            https://lean-lang.org/
Source0:        https://github.com/leanprover/lean4/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         lean4-ldflags-libgmp.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
ExcludeArch:    s390x %{ix86}
Provides:       %{name}-static = %{version}-%{release}

%description
Lean is a functional programming language that makes it easy to write
correct and maintainable code. You can also use Lean as an interactive
theorem prover. Lean programming primarily involves defining types and
functions. This allows your focus to remain on the problem domain and
manipulating its data, rather than the details of programming.


%prep
%autosetup -p1


%build
%cmake \
  -DLEAN_BUILD_TYPE="RELEASE" \
  -DUSE_GITHASH=OFF \
  -DLEAN_INSTALL_PREFIX=%{buildroot}
%cmake_build


%install
# cmake_install does not do anything
make -C redhat-linux-build/stage1 install

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
* Fri Jul 12 2024 Jens Petersen <petersen@redhat.com> - 4.9.1-1
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
