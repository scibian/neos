%define debug_package %{nil}

Summary: HPC job sessions manager framework
Name: neos
Version: 0.6.16
Release: 1%{?dist}.edf
Source0: %{name}-%{version}.tar.gz
License: GPLv3
Group: Application/System
Prefix: %{_prefix}
Vendor: EDF CCN HPC <dsp-cspito-ccn-hpc@edf.fr>
Url: https://github.com/scibian/%{__name}
BuildRequires: python3-setuptools, python3-sphinx, python3-sphinx_rtd_theme
Requires: neos-core, neos-scenarios-graphical, neos-slurm-graphical-plugins
%description
 This package contains the NEOS software which provides a generic framework to
 manage job sessions on HPC clusters.
 The framework is based on scenarios. A scenario defines the sequential steps
 to properly setup and initialize the job session. Users select the scenario
 for their jobs and can even define their own scenarios. The frawework can
 manage a wide variety of workloads from classic MPI parallel computing to
 advanced visualization sessions with 3D remote rendering.
 NEOS is fully integrated with open-source Slurm workload manager and modules
 environment manager.
 This package should be installed on all nodes (frontends as well as compute
 nodes).

%prep
%setup -q

# Build Section
%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=%{buildroot}
install -d %{buildroot}/etc/neos
install -d %{buildroot}/usr/lib/neos/exec
install -d %{buildroot}/usr/lib/neos/exec/contribs
install -m 644 conf/neos.conf %{buildroot}/etc/neos
ln -s %{python3_sitelib}/neos/scenarios %{buildroot}/usr/lib/neos/scenarios
install -m 755 scripts/* %{buildroot}/usr/lib/neos/exec/
install -m 755 contribs/restore-xorg-resolution.sh %{buildroot}/usr/lib/neos/exec/contribs

%clean
rm -rf %{buildroot}

%package core
Summary: NEOS core package
Requires: python3-clustershell, python3-pytz, python3-pyslurm
%description core
 NEOS core package

%package scenarios-graphical
Summary: NEOS scenarios for graphical nodes
Requires: neos-core, xorg-x11-xauth, xorg-x11-server-Xvfb, xorg-x11-utils, x11vnc
%description scenarios-graphical
 This package provides scenarios for NEOS to use on graphical nodes of a
 cluster. This includes scenarios for VNC (with Xfce4 and Gnome window
 managers), Paraview and Salome sessions.

%package slurm-graphical-plugins
Summary: NEOS Slurm plugins for graphical nodes
Requires: neos-core, slurm-llnl-generic-scripts-plugin, xorg-x11-utils
%description slurm-graphical-plugins
 This package contains all Slurm prolog/epilog scripts to install on graphical nodes.

%files
%exclude %{python3_sitelib}/tests

%files core
%config /etc/neos/neos.conf
/usr/bin/neos
/usr/lib/neos/exec/neos
/usr/lib/neos/exec/neos_inenv
%{python3_sitelib}/neos/*.py
%{python3_sitelib}/neos/__pycache__/*.pyc
%{python3_sitelib}/NEOS*egg-info/*


%files scenarios-graphical
/usr/lib/neos/scenarios
%{python3_sitelib}/neos/scenarios/*.py
%{python3_sitelib}/neos/scenarios/__pycache__/*.pyc

%files slurm-graphical-plugins
/usr/lib/neos/exec/contribs/restore-xorg-resolution.sh

%changelog
* Thu Feb 24 2022 Rémi Palancher <remi-externe.palancher@edf.fr> 0.6.16-1.el8.edf
- New upstream release 0.6.16
- Symlink scenarios instead of duplication
* Tue Feb 02 2021 Guillaume RANQUET <guillaume-externe.ranquet@edf.fr> 0.6.14
- Initial RPM release based on 0.6.14
