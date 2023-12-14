%global debug_package %{nil}

Name:           lean4
Version:        4.3.0
Release:        1%{?dist}
Summary:        Functional programming language and theorem prover

License:        Apache-2.0
URL:            https://lean-lang.org/
Source0:        https://github.com/leanprover/lean4/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

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
# does not do anything
#%%cmake_install
make -C redhat-linux-build/stage1 install
mkdir -p %{buildroot}%{_prefix}
rm %{buildroot}/lean-%{version}-linux/LICENSE*
for i in %{buildroot}/lean-%{version}-linux/*/; do
mv $i %{buildroot}%{_prefix}
done



%files
%license LICENSE
%doc CONTRIBUTING.md README.md RELEASES.md
%{_bindir}/*
%{_includedir}/lean
%{_prefix}/lib/lean
%{_datadir}/lean
%{_prefix}/src/lean


%changelog
* Tue Dec 12 2023 Jens Petersen <petersen@redhat.com>
- initial packaging
