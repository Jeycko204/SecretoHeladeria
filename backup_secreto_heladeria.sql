/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.1.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: secreto_heladeria_db
-- ------------------------------------------------------
-- Server version	12.1.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add proveedor',7,'add_proveedor'),
(26,'Can change proveedor',7,'change_proveedor'),
(27,'Can delete proveedor',7,'delete_proveedor'),
(28,'Can view proveedor',7,'view_proveedor'),
(29,'Can add categoria',8,'add_categoria'),
(30,'Can change categoria',8,'change_categoria'),
(31,'Can delete categoria',8,'delete_categoria'),
(32,'Can view categoria',8,'view_categoria'),
(33,'Can add compra',9,'add_compra'),
(34,'Can change compra',9,'change_compra'),
(35,'Can delete compra',9,'delete_compra'),
(36,'Can view compra',9,'view_compra'),
(37,'Can add orden compra',10,'add_ordencompra'),
(38,'Can change orden compra',10,'change_ordencompra'),
(39,'Can delete orden compra',10,'delete_ordencompra'),
(40,'Can view orden compra',10,'view_ordencompra'),
(41,'Can add detalle orden',11,'add_detalleorden'),
(42,'Can change detalle orden',11,'change_detalleorden'),
(43,'Can delete detalle orden',11,'delete_detalleorden'),
(44,'Can view detalle orden',11,'view_detalleorden'),
(45,'Can add evaluacion proveedor',12,'add_evaluacionproveedor'),
(46,'Can change evaluacion proveedor',12,'change_evaluacionproveedor'),
(47,'Can delete evaluacion proveedor',12,'delete_evaluacionproveedor'),
(48,'Can view evaluacion proveedor',12,'view_evaluacionproveedor'),
(49,'Can add insumo',13,'add_insumo'),
(50,'Can change insumo',13,'change_insumo'),
(51,'Can delete insumo',13,'delete_insumo'),
(52,'Can view insumo',13,'view_insumo'),
(53,'Can add Notificación',14,'add_notification'),
(54,'Can change Notificación',14,'change_notification'),
(55,'Can delete Notificación',14,'delete_notification'),
(56,'Can view Notificación',14,'view_notification'),
(57,'Can add Perfil de Usuario',15,'add_userprofile'),
(58,'Can change Perfil de Usuario',15,'change_userprofile'),
(59,'Can delete Perfil de Usuario',15,'delete_userprofile'),
(60,'Can view Perfil de Usuario',15,'view_userprofile');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$1000000$8gIb48ZrQaefOVQOH9DAzk$MZ09OXTiUZ9TF/9HlP8EpM2q2nioDBZZQWs/XZaFgMs=','2025-12-16 12:46:29.736727',1,'root','','','root@mail.cl',1,1,'2025-12-16 12:40:55.265413');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(8,'compras','categoria'),
(9,'compras','compra'),
(11,'compras','detalleorden'),
(12,'compras','evaluacionproveedor'),
(13,'compras','insumo'),
(14,'compras','notification'),
(10,'compras','ordencompra'),
(7,'compras','proveedor'),
(15,'compras','userprofile'),
(5,'contenttypes','contenttype'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-12-16 12:40:05.013325'),
(2,'auth','0001_initial','2025-12-16 12:40:05.369931'),
(3,'admin','0001_initial','2025-12-16 12:40:05.450365'),
(4,'admin','0002_logentry_remove_auto_add','2025-12-16 12:40:05.458303'),
(5,'admin','0003_logentry_add_action_flag_choices','2025-12-16 12:40:05.467433'),
(6,'contenttypes','0002_remove_content_type_name','2025-12-16 12:40:05.539234'),
(7,'auth','0002_alter_permission_name_max_length','2025-12-16 12:40:05.576535'),
(8,'auth','0003_alter_user_email_max_length','2025-12-16 12:40:05.601624'),
(9,'auth','0004_alter_user_username_opts','2025-12-16 12:40:05.608385'),
(10,'auth','0005_alter_user_last_login_null','2025-12-16 12:40:05.650485'),
(11,'auth','0006_require_contenttypes_0002','2025-12-16 12:40:05.652809'),
(12,'auth','0007_alter_validators_add_error_messages','2025-12-16 12:40:05.661134'),
(13,'auth','0008_alter_user_username_max_length','2025-12-16 12:40:05.693793'),
(14,'auth','0009_alter_user_last_name_max_length','2025-12-16 12:40:05.726548'),
(15,'auth','0010_alter_group_name_max_length','2025-12-16 12:40:05.754592'),
(16,'auth','0011_update_proxy_permissions','2025-12-16 12:40:05.764663'),
(17,'auth','0012_alter_user_first_name_max_length','2025-12-16 12:40:05.793053'),
(18,'compras','0001_initial','2025-12-16 12:40:05.860955'),
(19,'compras','0002_alter_ingrediente_cantidad','2025-12-16 12:40:05.922916'),
(20,'compras','0003_categoriaproveedor_proveedor_categoria','2025-12-16 12:40:05.973977'),
(21,'compras','0004_rename_categoriaproveedor_categoria_and_more','2025-12-16 12:40:06.151511'),
(22,'compras','0005_proveedor_categoria_proveedor_certificacion_and_more','2025-12-16 12:40:06.729691'),
(23,'compras','0006_insumo','2025-12-16 12:40:06.778420'),
(24,'compras','0007_compra_correo_contacto_compra_direccion_entrega_and_more','2025-12-16 12:40:06.954794'),
(25,'compras','0008_change_compra_proveedor_on_delete','2025-12-16 12:40:07.047183'),
(26,'compras','0009_add_proveedor_nombre_and_populate','2025-12-16 12:40:07.095474'),
(27,'compras','0010_alter_compra_proveedor_nombre','2025-12-16 12:40:07.100317'),
(28,'compras','0011_rename_proveedor_nombre_to_nombre_proveedor','2025-12-16 12:40:07.123741'),
(29,'compras','0012_remove_compra_insumos_alter_compra_nombre_proveedor_and_more','2025-12-16 12:40:07.151843'),
(30,'compras','0012_alter_compra_nombre_proveedor','2025-12-16 12:40:07.156027'),
(31,'compras','0013_merge_20251106_0106','2025-12-16 12:40:07.157968'),
(32,'compras','0014_alter_proveedor_tiempo_entrega_ordencompra_and_more','2025-12-16 12:40:07.250140'),
(33,'compras','0015_evaluacionproveedor','2025-12-16 12:40:07.346669'),
(34,'compras','0016_ordencompra_iva_ordencompra_neto_and_more','2025-12-16 12:40:07.479769'),
(35,'compras','0017_remove_ordencompra_proveedor_detalleorden_proveedor','2025-12-16 12:40:07.614374'),
(36,'compras','0018_ordencompra_fecha_anulacion_and_more','2025-12-16 12:40:07.758414'),
(37,'compras','0019_alter_detalleorden_insumo_insumo_and_more','2025-12-16 12:40:08.004270'),
(38,'compras','0020_proveedor_agregar_contacto_secundario_and_more','2025-12-16 12:40:08.337840'),
(39,'compras','0021_alter_proveedor_categoria','2025-12-16 12:40:08.461186'),
(40,'compras','0022_alter_ordencompra_estado_notification_userprofile','2025-12-16 12:40:08.611818'),
(41,'compras','0023_alter_ordencompra_estado','2025-12-16 12:40:08.623545'),
(42,'compras','0024_ordencompra_updated_at_alter_ordencompra_estado','2025-12-16 12:40:08.685725'),
(43,'compras','0025_alter_ordencompra_estado_alter_proveedor_categoria','2025-12-16 12:40:08.714276'),
(44,'sessions','0001_initial','2025-12-16 12:40:08.757363'),
(45,'compras','0026_alter_categoria_table_alter_compra_table_and_more','2025-12-16 13:06:12.122422');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `django_session` VALUES
('kfrwedmbzkgh5c5tdlqgyepfuk9xqxnm','.eJxVjEEOwiAQRe_C2pABWmBcuu8ZyAxQqRqalHZlvLsh6UK3_7333yLQsZdwtLyFJYmrUOLyuzHFZ64dpAfV-yrjWvdtYdkVedImpzXl1-10_w4KtdJr7ZkdeY2eDHK2auZZQXQIDhIiqdGgBz8oPWhyYNgmo4dxTtYDEojPF9IjNuM:1vVURh:fbwOpgVlBLcw46Ri6_X1G-42HhUH0R_gExcQRNZpCG4','2025-12-30 12:46:29.739349');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_categoria`
--

DROP TABLE IF EXISTS `zwt_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_categoria` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_categoria`
--

LOCK TABLES `zwt_categoria` WRITE;
/*!40000 ALTER TABLE `zwt_categoria` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `zwt_categoria` VALUES
(3,'Envases'),
(2,'Frutas'),
(1,'Lácteos'),
(5,'Maquinaria'),
(4,'Saborizantes');
/*!40000 ALTER TABLE `zwt_categoria` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_compra`
--

DROP TABLE IF EXISTS `zwt_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_compra` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `numero_factura` varchar(50) NOT NULL,
  `fecha_compra` date NOT NULL,
  `monto_total` decimal(12,0) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `proveedor_id` bigint(20) DEFAULT NULL,
  `correo_contacto` varchar(254) NOT NULL,
  `direccion_entrega` varchar(255) NOT NULL,
  `nombre_proveedor` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_factura` (`numero_factura`),
  KEY `compras_compra_proveedor_id_d647dfa3_fk_compras_proveedor_id` (`proveedor_id`),
  CONSTRAINT `compras_compra_proveedor_id_d647dfa3_fk_compras_proveedor_id` FOREIGN KEY (`proveedor_id`) REFERENCES `zwt_proveedor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_compra`
--

LOCK TABLES `zwt_compra` WRITE;
/*!40000 ALTER TABLE `zwt_compra` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `zwt_compra` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_detalle_orden`
--

DROP TABLE IF EXISTS `zwt_detalle_orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_detalle_orden` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `insumo` varchar(200) NOT NULL,
  `unidad_medida` varchar(50) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `precio_unitario` decimal(12,0) NOT NULL,
  `subtotal` decimal(12,0) NOT NULL,
  `fecha` date NOT NULL,
  `orden_id` bigint(20) NOT NULL,
  `proveedor_id` bigint(20) NOT NULL,
  `insumo_fk_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `compras_detalleorden_orden_id_13e6ae29_fk_compras_ordencompra_id` (`orden_id`),
  KEY `compras_detalleorden_proveedor_id_ca7ab058_fk_compras_p` (`proveedor_id`),
  KEY `compras_detalleorden_insumo_fk_id_7a7c26e6_fk_compras_insumo_id` (`insumo_fk_id`),
  CONSTRAINT `compras_detalleorden_insumo_fk_id_7a7c26e6_fk_compras_insumo_id` FOREIGN KEY (`insumo_fk_id`) REFERENCES `zwt_insumo` (`id`),
  CONSTRAINT `compras_detalleorden_orden_id_13e6ae29_fk_compras_ordencompra_id` FOREIGN KEY (`orden_id`) REFERENCES `zwt_orden_compra` (`id`),
  CONSTRAINT `compras_detalleorden_proveedor_id_ca7ab058_fk_compras_p` FOREIGN KEY (`proveedor_id`) REFERENCES `zwt_proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_detalle_orden`
--

LOCK TABLES `zwt_detalle_orden` WRITE;
/*!40000 ALTER TABLE `zwt_detalle_orden` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `zwt_detalle_orden` VALUES
(1,'Cucharas Plásticas','Unidades',33.00,2385,78705,'2025-12-16',1,3,6),
(2,'Vasos 200ml','Unidades',42.00,1649,69258,'2025-12-16',1,3,5),
(3,'Vasos 200ml','Unidades',97.00,4688,454736,'2025-12-16',1,3,5),
(4,'Leche Entera','Litros',41.00,3569,146329,'2025-12-16',2,1,1),
(5,'Leche Entera','Litros',80.00,2567,205360,'2025-12-16',2,1,1),
(6,'Crema de Leche','Litros',73.00,4579,334267,'2025-12-16',3,1,2),
(7,'Leche Entera','Litros',81.00,4441,359721,'2025-12-16',3,1,1),
(8,'Crema de Leche','Litros',93.00,3931,365583,'2025-12-16',4,1,2),
(9,'Crema de Leche','Litros',75.00,3159,236925,'2025-12-16',4,1,2),
(10,'Leche Entera','Litros',30.00,4014,120420,'2025-12-16',4,1,1),
(11,'Cucharas Plásticas','Unidades',16.00,2937,46992,'2025-12-16',5,3,6),
(12,'Vasos 200ml','Unidades',22.00,2829,62238,'2025-12-16',5,3,5),
(13,'Cucharas Plásticas','Unidades',72.00,3663,263736,'2025-12-16',5,3,6);
/*!40000 ALTER TABLE `zwt_detalle_orden` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_evaluacion_proveedor`
--

DROP TABLE IF EXISTS `zwt_evaluacion_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_evaluacion_proveedor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `calidad` varchar(20) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion` longtext NOT NULL,
  `proveedor_id` bigint(20) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `compras_evaluacionpr_proveedor_id_33e01811_fk_compras_p` (`proveedor_id`),
  KEY `compras_evaluacionproveedor_usuario_id_8ddb3b99_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `compras_evaluacionpr_proveedor_id_33e01811_fk_compras_p` FOREIGN KEY (`proveedor_id`) REFERENCES `zwt_proveedor` (`id`),
  CONSTRAINT `compras_evaluacionproveedor_usuario_id_8ddb3b99_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_evaluacion_proveedor`
--

LOCK TABLES `zwt_evaluacion_proveedor` WRITE;
/*!40000 ALTER TABLE `zwt_evaluacion_proveedor` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `zwt_evaluacion_proveedor` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_insumo`
--

DROP TABLE IF EXISTS `zwt_insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_insumo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `unidad_medida` varchar(50) NOT NULL,
  `categoria_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compras_insumo_categoria_id_e7835585_fk_compras_categoria_id` (`categoria_id`),
  CONSTRAINT `compras_insumo_categoria_id_e7835585_fk_compras_categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `zwt_categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_insumo`
--

LOCK TABLES `zwt_insumo` WRITE;
/*!40000 ALTER TABLE `zwt_insumo` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `zwt_insumo` VALUES
(1,'Leche Entera','Litros',1),
(2,'Crema de Leche','Litros',1),
(3,'Frutillas','Kilos',2),
(4,'Plátanos','Kilos',2),
(5,'Vasos 200ml','Unidades',3),
(6,'Cucharas Plásticas','Unidades',3),
(7,'Esencia Vainilla','Litros',4),
(8,'Cacao en Polvo','Kilos',4);
/*!40000 ALTER TABLE `zwt_insumo` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_notification`
--

DROP TABLE IF EXISTS `zwt_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_notification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `notification_type` varchar(20) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `orden_compra_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compras_notification_orden_compra_id_e9cfa042_fk_compras_o` (`orden_compra_id`),
  KEY `compras_notification_user_id_8fb3d385_fk_auth_user_id` (`user_id`),
  CONSTRAINT `compras_notification_orden_compra_id_e9cfa042_fk_compras_o` FOREIGN KEY (`orden_compra_id`) REFERENCES `zwt_orden_compra` (`id`),
  CONSTRAINT `compras_notification_user_id_8fb3d385_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_notification`
--

LOCK TABLES `zwt_notification` WRITE;
/*!40000 ALTER TABLE `zwt_notification` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `zwt_notification` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_orden_compra`
--

DROP TABLE IF EXISTS `zwt_orden_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_orden_compra` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha_emision` date NOT NULL,
  `monto_total` decimal(12,0) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `iva` decimal(12,0) NOT NULL,
  `neto` decimal(12,0) NOT NULL,
  `solicitante_id` int(11) DEFAULT NULL,
  `fecha_anulacion` datetime(6) DEFAULT NULL,
  `motivo_anulacion` longtext DEFAULT NULL,
  `usuario_anulo_id` int(11) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compras_ordencompra_solicitante_id_6a96d738_fk_auth_user_id` (`solicitante_id`),
  KEY `compras_ordencompra_usuario_anulo_id_73b4d9bc_fk_auth_user_id` (`usuario_anulo_id`),
  CONSTRAINT `compras_ordencompra_solicitante_id_6a96d738_fk_auth_user_id` FOREIGN KEY (`solicitante_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `compras_ordencompra_usuario_anulo_id_73b4d9bc_fk_auth_user_id` FOREIGN KEY (`usuario_anulo_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_orden_compra`
--

LOCK TABLES `zwt_orden_compra` WRITE;
/*!40000 ALTER TABLE `zwt_orden_compra` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `zwt_orden_compra` VALUES
(1,'2025-12-16',717212,'EN_ESPERA',114513,602699,1,NULL,NULL,NULL,'2025-12-16 12:43:42.764738'),
(2,'2025-12-16',418510,'EN_ESPERA',66821,351689,1,NULL,NULL,NULL,'2025-12-16 12:43:42.780486'),
(3,'2025-12-16',825846,'EN_ESPERA',131858,693988,1,NULL,NULL,NULL,'2025-12-16 12:43:42.795219'),
(4,'2025-12-16',860284,'EN_ESPERA',137356,722928,1,NULL,NULL,NULL,'2025-12-16 12:43:42.815112'),
(5,'2025-12-16',443830,'EN_ESPERA',70864,372966,1,NULL,NULL,NULL,'2025-12-16 12:43:42.833675');
/*!40000 ALTER TABLE `zwt_orden_compra` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_proveedor`
--

DROP TABLE IF EXISTS `zwt_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_proveedor` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `contacto` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `categoria_id` bigint(20) DEFAULT NULL,
  `certificacion` varchar(100) DEFAULT NULL,
  `dias_entrega` varchar(50) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `monto_minimo` decimal(12,0) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `tiempo_entrega` int(10) unsigned NOT NULL CHECK (`tiempo_entrega` >= 0),
  `agregar_contacto_secundario` tinyint(1) NOT NULL,
  `contacto_secundario_apellido` varchar(100) NOT NULL,
  `contacto_secundario_direccion` varchar(255) NOT NULL,
  `contacto_secundario_email` varchar(254) NOT NULL,
  `contacto_secundario_nombre` varchar(100) NOT NULL,
  `contacto_secundario_rut` varchar(12) NOT NULL,
  `contacto_secundario_telefono` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rut` (`rut`),
  KEY `compras_proveedor_categoria_id_c3df2504_fk_compras_categoria_id` (`categoria_id`),
  CONSTRAINT `compras_proveedor_categoria_id_c3df2504_fk_compras_categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `zwt_categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_proveedor`
--

LOCK TABLES `zwt_proveedor` WRITE;
/*!40000 ALTER TABLE `zwt_proveedor` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `zwt_proveedor` VALUES
(1,'Lácteos del Sur','Juan Perez','+56912345678',1,'','Lunes, Jueves','Av. Siempre Viva 123','lacteos@example.com',50000,'76.123.456-1',2,0,'','','','','',''),
(2,'Frutas Frescas SpA','Maria Gonzalez','+56912345678',2,'','Lunes, Jueves','Av. Siempre Viva 123','frutas@example.com',50000,'77.234.567-2',2,0,'','','','','',''),
(3,'Envases Chile','Carlos Ruiz','+56912345678',3,'','Lunes, Jueves','Av. Siempre Viva 123','envases@example.com',50000,'78.345.678-3',2,0,'','','','','',''),
(4,'Sabores Globales','Ana Lopez','+56912345678',4,'','Lunes, Jueves','Av. Siempre Viva 123','sabores@example.com',50000,'79.456.789-4',2,0,'','','','','','');
/*!40000 ALTER TABLE `zwt_proveedor` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_proveedor_insumos`
--

DROP TABLE IF EXISTS `zwt_proveedor_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_proveedor_insumos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `proveedor_id` bigint(20) NOT NULL,
  `insumo_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `compras_proveedor_insumos_proveedor_id_insumo_id_3305c9d9_uniq` (`proveedor_id`,`insumo_id`),
  KEY `compras_proveedor_in_insumo_id_5dbc71bf_fk_compras_i` (`insumo_id`),
  CONSTRAINT `compras_proveedor_in_insumo_id_5dbc71bf_fk_compras_i` FOREIGN KEY (`insumo_id`) REFERENCES `zwt_insumo` (`id`),
  CONSTRAINT `compras_proveedor_in_proveedor_id_54101319_fk_compras_p` FOREIGN KEY (`proveedor_id`) REFERENCES `zwt_proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_proveedor_insumos`
--

LOCK TABLES `zwt_proveedor_insumos` WRITE;
/*!40000 ALTER TABLE `zwt_proveedor_insumos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `zwt_proveedor_insumos` VALUES
(1,1,1),
(2,1,2),
(3,2,3),
(4,2,4),
(5,3,5),
(6,3,6),
(8,4,7),
(7,4,8);
/*!40000 ALTER TABLE `zwt_proveedor_insumos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `zwt_user_profile`
--

DROP TABLE IF EXISTS `zwt_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `zwt_user_profile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `department` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `compras_userprofile_user_id_54581b38_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zwt_user_profile`
--

LOCK TABLES `zwt_user_profile` WRITE;
/*!40000 ALTER TABLE `zwt_user_profile` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `zwt_user_profile` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-12-16 10:28:42
