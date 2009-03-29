%define compat_python %{_bindir}/python2.4

%{!?python_sitelib: %define python_sitelib %(%{compat_python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{compat_python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define     _upstream_nvr   elementtree-1.2.6-20050316
%define     _upstream_cnvr  cElementTree-1.0.5-20051216    

Name: compat-python24-elementtree
Version: 1.2.6
Release: 7%{?dist}
Summary: Fast XML parser and writer
Group: Development/Libraries
License: PSF
URL: http://effbot.org/zone/element-index.htm
Source0: http://effbot.org/downloads/%{_upstream_nvr}.zip
Source1: http://effbot.org/downloads/%{_upstream_cnvr}.tar.gz
Source2: cElementTree-system-expat-setup.py
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: expat-devel, compat-python24-devel, compat-python24
Requires: python-abi = 2.4

%description
The Element type is a simple but flexible container object, designed
to store hierarchical data structures, such as simplified XML
infosets, in memory. The element type can be described as a cross
between a Python list and a Python dictionary.

This package also includes the C implementation, %{_upstream_cnvr}.

%prep
%setup -q -n %{_upstream_nvr} -a 1

## Take care of cElementTree
pushd %{_upstream_cnvr}
mv -f setup.py setup.py-orig
cp -f %{SOURCE2} setup.py
cp -f README ../README-cElementTree
cp -f CHANGES ../CHANGES-cElementTree
popd


%build
%{compat_python} setup.py build
pushd %{_upstream_cnvr}
CFLAGS="$RPM_OPT_FLAGS" %{compat_python} setup.py build
popd


%install
rm -rf $RPM_BUILD_ROOT
%{compat_python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
pushd %{_upstream_cnvr}
%{compat_python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs samples README* CHANGES* benchmark.py
%dir %{python_sitelib}/elementtree
%{python_sitelib}/elementtree/*.py*
%{python_sitearch}/*.so

%changelog
* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.2.6-7
- rebuild for new F11 features

* Sun Aug 10 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.2.6-6
- rebuild for RPM Fusion

* Mon Sep 3 2007 Jonathan Steffan <jon a fedoraunity.org> 1.2.6-5
- Initial RPM release

