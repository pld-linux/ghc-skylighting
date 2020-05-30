#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	skylighting
Summary:	Syntax highlighting library
Name:		ghc-%{pkgname}
Version:	0.8.4
Release:	1
License:	GPL v2
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/skylighting
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	1894daff506baf4f91c63b3953bdd2da
URL:		http://hackage.haskell.org/package/skylighting
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-blaze-html
BuildRequires:	ghc-pretty-show
BuildRequires:	ghc-skylighting-core
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-blaze-html-prof
BuildRequires:	ghc-pretty-show-prof
BuildRequires:	ghc-skylighting-core-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-blaze-html
Requires:	ghc-pretty-show
Requires:	ghc-skylighting-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Skylighting is a syntax highlighting library with support for over one
hundred languages. It derives its tokenizers from XML syntax
definitions used by KDE's KSyntaxHighlighting framework, so any syntax
supported by that framework can be added. An optional command-line
program is provided. Skylighting is intended to be the successor to
highlighting-kate. This package provides generated syntax modules
based on the KDE XML definitions provided by the skylighting-core
package. As a result this package is licensed under the GPL.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-blaze-html-prof
Requires:	ghc-pretty-show-prof
Requires:	ghc-skylighting-core-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.md changelog.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Syntax
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Syntax/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Syntax/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Skylighting/Syntax/*.p_hi
%endif
