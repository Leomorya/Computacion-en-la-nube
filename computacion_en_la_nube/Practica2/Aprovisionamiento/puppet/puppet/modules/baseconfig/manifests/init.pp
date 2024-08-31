class baseconfig {

  # Actualizar los repositorios de apt
  exec { 'apt-get update':
    command => '/usr/bin/apt-get update',
  }

  # Instalar paquetes necesarios
  package { ['apache2', 'tree', 'python3-pip']:
    ensure => present,
  }

  # Instalar Jupyter Notebook con pip
  exec { 'install-jupyter':
    command => '/usr/bin/pip3 install jupyter',
    require => Package['python3-pip'],
  }

  # Configura el PATH de Jupyter
  exec { 'set-path':
    command => 'echo \'export PATH="$HOME/.local/bin:$PATH"\' >> /etc/profile.d/jupyter.sh',
    path    => '/usr/local/bin:/usr/bin:/bin',
    require => Exec['install-jupyter'],
  }

  # Crear archivo index.html en el directorio de Apache
  file { '/var/www/html/index.html':
    ensure  => present,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    source  => 'puppet:///modules/baseconfig/index.html',
  }

  # Asegurarse de que Apache esté corriendo
  service { 'apache2':
    ensure  => running,
    enable  => true,
    require => Package['apache2'],
  }

}

