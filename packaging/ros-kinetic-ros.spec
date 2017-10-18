Name:           ros-kinetic-ros
Version:        1.14.1
Release:        0%{?dist}
License:        BSD
Summary:        ROS packaging system
Url:            http://www.ros.org/wiki/ROS
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ros-kinetic-rospack
BuildRequires:  ros-kinetic-catkin
Requires:       ros-kinetic-catkin
Requires:       ros-kinetic-rosmake
Requires:       ros-kinetic-rosunit
Requires:       ros-kinetic-roscreate
Requires:       ros-kinetic-rosclean
Requires:       ros-kinetic-rosboost-cfg
Requires:       ros-kinetic-rosbash
Requires:       ros-kinetic-mk
Requires:       ros-kinetic-rosbuild
Requires:       ros-kinetic-roslang
Requires:       ros-kinetic-roslib
Requires:       ros-kinetic-rospack

%description
Robot Operating System (ROS)
ROS is a meta-operating system for your robot. It provides
language-independent and network-transparent communication for a
distributed robot control system.

%prep
%setup -q
cp %{SOURCE1001} .

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh"  ]; then . "/usr/setup.sh"; fi

### helper function ###
do_build()
{
   echo "[do_build] Entering build dir: ${1}"
    pushd ${1}
    mkdir build
    pushd build
    cmake .. \
        -DCMAKE_INSTALL_PREFIX="$CMAKE_PREFIX_PATH" \
        -DCMAKE_PREFIX_PATH="$CMAKE_PREFIX_PATH" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1"
    make %{?_smp_mflags}
    popd
    popd
   echo "[do_build] Leaving : ${1}"
}

### build ros tools ###
for i in `ls tools`
do
   do_build "tools/$i"
done

### build ros core ###
for i in `ls core`
do
   do_build "core/$i"
done

### build ros ###
do_build ros

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/usr/setup.sh"  ]; then . "/usr/setup.sh"; fi

### helper function ###
do_install()
{
    echo "[do_install] Entering install package dir: $i"
    pushd ${1}/build
    make install DESTDIR=%{buildroot}
   
    %define local_install_dir  $(pwd)
    make install DESTDIR=%{local_install_dir}/installed
    find installed -type f  | sed 's/installed//' >  install_manifest.txt
    popd
    echo "[do_install] Leaving : $i"
}

### install ros tools ###
for i in `ls tools`
do
   do_install  "tools/$i"
done

### install ros core ###
for i in `ls core`
do
   do_install "core/$i"
done

### install ros ###
do_install ros

%post

%postun

%files -f ros/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n     %{name}make 
Summary:        ROS build tool
Group:          Development/Libraries
%description -n %{name}make
rosmake is a ros dependency aware build tool which can be used to build all dependencies in the correct order.

%files -n %{name}make -f tools/rosmake/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n     %{name}unit
Summary:        Unit-testing package for ROS
Group:          Development/Libraries
%description -n %{name}unit
Unit-testing package for ROS. This is a lower-level library for rostest and handles unit tests,
whereas rostest  handles integration tests.

%files -n %{name}unit -f tools/rosunit/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n %{name}create
Summary:        Tools used in the creation of ROS filesystem resources
Group:          Development/Libraries
%description -n %{name}create
roscreate contains a tool that assists in the creation of ROS filesystem resources. It provides: roscreate-pkg, which creates a new package directory, including the appropriate build and manifest files.

%files -n %{name}create -f tools/roscreate/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n     %{name}clean
Summary:        A tool for cleanup filesystem resources (e.g. log files)
Group:          Development/Libraries
%description -n %{name}clean
%{summary}.

%files -n %{name}clean -f tools/rosclean/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n %{name}boost-cfg
Summary:        Contains scripts used by the rosboost-cfg tool
Group:          Development/Libraries
%description -n %{name}boost-cfg
Contains scripts used by the rosboost-cfg tool for determining cflags/lflags/etc. of boost on your system

%files -n %{name}boost-cfg -f tools/rosboost_cfg/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n %{name}bash
Summary:        Assorted shell commands for using ros with bash
Group:          Development/Libraries
%description -n %{name}bash
%{summary}.

%files -n %{name}bash -f tools/rosbash/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n ros-%{ros_distro}-mk
Summary:        A collection of .mk include files for building ROS architectural elements
Group:          Development/Libraries
%description -n ros-%{ros_distro}-mk
A collection of .mk include files for building ROS architectural elements. Most package authors should use cmake .mk, which calls CMake for the build of the package. The other files in this package are intended for use in exotic situations that mostly arise when importing 3rdparty code.

%files -n ros-%{ros_distro}-mk -f core/mk/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n %{name}build
Summary:        Contains scripts for managing the CMake-based build system
Group:          Development/Libraries
%description -n %{name}build
rosbuild contains scripts for managing the CMake-based build system for ROS.

%files -n %{name}build -f core/rosbuild/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n %{name}lang
Summary:        A common package that all ROS client libraries depend on 
Group:          Development/Libraries
%description -n %{name}lang
roslang is a common package that all ROS client libraries depend on. This is mainly used to find client libraries (via 'rospack depends-on1 roslang').

%files -n %{name}lang -f core/roslang/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%package -n %{name}lib
Summary:        Base dependencies and support libraries for ROS
Group:          Development/Libraries
%description -n %{name}lib
Base dependencies and support libraries for ROS. roslib contains many of the common data structures and tools that are shared across ROS client library implementations.

%files -n %{name}lib -f core/roslib/build/install_manifest.txt
%manifest %{name}.manifest
%defattr(-,root,root)

%changelog
* Wed Mar 29 2017 Zhang Xingtao <xingtao.zhang@yahhoo.com> - 1.13.5
* Fri May 09 2014 Dirk Thomas <dthomas@osrfoundation.org> - 1.10.6-0
