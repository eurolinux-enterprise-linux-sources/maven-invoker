Name:           maven-invoker
Version:        2.1.1
Release:        7%{?dist}
Summary:        Fires a maven build in a clean environment
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-invoker/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Patch0:         %{name}-MSHARED-278.patch
Patch1:         %{name}-MSHARED-279.patch

BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  junit
BuildRequires:  maven-local
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-shared
Requires:       java
Requires:       jpackage-utils
Requires:       maven-shared
Requires:       plexus-containers-component-annotations
Requires:       plexus-utils

Obsoletes:      maven-shared-invoker < %{version}-%{release}
Provides:       maven-shared-invoker = %{version}-%{release}

%description
This API is concerned with firing a Maven build in a new JVM. It accomplishes
its task by building up a conventional Maven command line from options given in
the current request, along with those global options specified in the invoker
itself. Once it has the command line, the invoker will execute it, and capture
the resulting exit code or any exception thrown to signal a failure to execute.
Input/output control can be specified using an InputStream and up to two
InvocationOutputHandlers.

This is a replacement package for maven-shared-invoker

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils
    
%description javadoc
API documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
mvn-rpmbuild package javadoc:aggregate -Dmaven.test.failure.ignore

%install
# JAR
install -Ddm 755 %{buildroot}/%{_javadir}
install -Dpm 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# POM
install -Ddm 755 %{buildroot}/%{_mavenpomdir}
install -Dpm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# JavaDoc
install -Ddm 755 %{buildroot}/%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%doc LICENSE NOTICE
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE NOTICE
%doc %{_javadocdir}/%{name}


%changelog
* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-7
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Mar 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1.1-6
- Add patch for MSHARED-278, resolves rhbz#921068
- Add patch for MSHARED-279, resolves rhbz#921067

* Wed Feb 20 2013 Tomas Radej <tradej@redhat.com> - 2.1.1-5
- Added B/R on maven-shared

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.1.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Jan 14 2013 Tomas Radej <tradej@redhat.com> - 2.1.1-2
- Disabled tests

* Fri Jan 11 2013 Tomas Radej <tradej@redhat.com> - 2.1.1-1
- Initial version

