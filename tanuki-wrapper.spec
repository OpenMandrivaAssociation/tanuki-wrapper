#%undefine _debugsource_packages

Name:     tanuki-wrapper
Version:  3.6.4
Release:  1
Summary:  Java Service Wrapper
URL:      https://wrapper.tanukisoftware.com
License:  GPLv3

Source0:  https://sourceforge.net/projects/wrapper/files/wrapper_src/Wrapper_3.6.4_20251218/wrapper_3.6.4_src.tar.gz/download#/%{name}_%{version}.tar.gz

Patch0:  build-only-wrapper.patch

BuildRequires:  ant
BuildRequires:  jdk-current
BuildRequires:  make
BuildRequires:  pkgconfig(cunit)
BuildRequires:  pkgconfig(ncursesw)

Requires:  curl
Requires:  git
Requires:  jre-current

%description
Configurable tool which allows Java applications to be installed and controlled like services.
Includes fault correction software to automatically restart crashed or frozen JVMs.
Critical when app is needed 24x7. Built for flexibility.

%prep
%autosetup -n wrapper_%{version}_src -p 1

%build
. /etc/profile.d/90java.sh
JAVA_VERSION=$(java -version 2>&1|head -n1 |cut -d' ' -f3 |sed -e 's,\",,g;s,-.*,,')
JAVA_MAJOR=$(echo ${JAVA_VERSION} |cut -d. -f1)

%ifarch %{ix86} %{arm} %{riscv32}
BITS=32
%else
BITS=64
%endif

ant -f build.xml jar:wrapper-only compile-c-unix -Dbits=$BITS -Dant.java.version=$JAVA_VERSION -Djavac.target.version=$JAVA_MAJOR

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}

mv bin/* %{buildroot}%{_bindir}/%{name}
mv lib/* %{buildroot}%{_libdir}/%{name}/

%files
%doc README_*.txt doc/revisions.txt doc/index.html
%doc src/conf/wrapper.conf.in
%license doc/wrapper-community-license-1.3.txt
%{_bindir}/%{name}
%{_libdir}/%{name}
