# Empty file debugsourcefiles.list
%global debug_package %{nil}

Name:           lean4
Version:        4.7.0
Release:        2%{?dist}
Summary:        Functional programming language and theorem prover

License:        Apache-2.0
URL:            https://lean-lang.org/
Source0:        https://github.com/leanprover/lean4/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
ExcludeArch:    s390x %{ix86}

%description
Lean is a functional programming language that makes it easy to write
correct and maintainable code. You can also use Lean as an interactive
theorem prover. Lean programming primarily involves defining types and
functions. This allows your focus to remain on the problem domain and
manipulating its data, rather than the details of programming.


%prep
%autosetup


%build
%cmake -DLEAN_BUILD_TYPE="Release" -DUSE_GITHASH=OFF -DLEAN_INSTALL_PREFIX=%{buildroot}
%cmake_build


%install
# cmake_install does not do anything
make -C redhat-linux-build/stage1 install
mkdir -p %{buildroot}%{_prefix}
rm %{buildroot}/lean-%{version}-linux/LICENSE*
for i in %{buildroot}/lean-%{version}-linux/*/; do
mv $i %{buildroot}%{_prefix}
done

strip %{buildroot}%{_bindir}/{lake,lean,leanc}
chmod a+x %{buildroot}%{_prefix}/lib/lean/lib*shared.so
strip %{buildroot}%{_prefix}/lib/lean/lib*shared.so


%files
%license LICENSE
%doc CONTRIBUTING.md README.md RELEASES.md
%{_bindir}/*
%{_includedir}/lean
%{_prefix}/lib/lean
%{_datadir}/lean
%{_prefix}/src/lean


%changelog
* Tue Apr 30 2024 Jens Petersen <petersen@redhat.com> - 4.7.0-2
- strip bin and lib*.so files

* Mon Apr 29 2024 Jens Petersen <petersen@redhat.com> - 4.7.0-1
- https://github.com/leanprover/lean4/releases/tag/v4.7.0
- https://lean-lang.org/blog/2024-4-4-lean-470/

* Tue Dec 12 2023 Jens Petersen <petersen@redhat.com> - 4.3.0.-1
- initial packaging
