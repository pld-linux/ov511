#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	Linux OVCam Drivers
Summary(pl):	Linuksowe sterowniki do kamer OVCam
Name:		ov511
Version:	2.32
Release:	%{_rel}
License:	GPL
Group:		Applications/Multimedia
Source0:	http://ovcam.org/ov511/download/2.xx/distros/%{name}-%{version}.tar.bz2
# Source0-md5:	6a08025311649356242761641a1df0f2
URL:		http://ovcam.org/ov511/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_module_suffix	experimental
%define	_module_dir	kernel/drivers/media/video

%description
Linux OVCam Drivers.

%description -l pl
Linuksowe sterowniki do kamer OVCam.

%package -n kernel%{_alt_kernel}-video-%{name}
Summary:	Linux driver for OVCam webcams
Summary(pl):	Sterownik dla Linuksa do kamer internetowych OVCam
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-video-%{name}
This is driver for OVCam webcams for Linux.

%description -n kernel%{_alt_kernel}-video-%{name} -l pl
Sterownik dla Linuksa do kamer internetowych OVCam.

%package -n kernel%{_alt_kernel}-smp-video-%{name}
Summary:	Linux SMP driver for OVCam webcams
Summary(pl):	Sterownik dla Linuksa SMP do kamer internetowych OVCam
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-video-%{name}
This is driver for OVCam webcams for Linux SMP.

%description -n kernel%{_alt_kernel}-smp-video-%{name} -l pl
Sterownik dla Linuksa SMP do kamer internetowych OVCam.

%prep
%setup -q
sed -i -e '/#include <linux.videodev.h>/a #include <media/v4l2-dev.h>' \
	*.[hc]
sed -e '/EXTRA_CFLAGS/s/$/ -DHAVE_V4L2 -DCONFIG_VIDEO_PROC_FS/' -i Makefile

%build
%if %{with kernel}
%build_kernel_modules -m ovcamchip,ov511,ovfx2,saa7111-new,tda7313
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -s %{_module_suffix} -n %{name} -m ovcamchip,ov511 -d %{_module_dir}
# no need to rename those:
%install_kernel_modules -m ovfx2,saa7111-new,tda7313 -d %{_module_dir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-video-%{name}
%depmod %{_kernel_ver}

%post -n kernel%{_alt_kernel}-smp-video-%{name}
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-video-%{name}
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/%{_module_dir}/*.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}/%{name}.conf

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-video-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/%{_module_dir}/*.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}smp/%{name}.conf
%endif
%endif
