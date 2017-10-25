-- MySQL dump 10.13  Distrib 5.7.19, for osx10.12 (x86_64)
--
-- Host: localhost    Database: mingjia
-- ------------------------------------------------------
-- Server version	5.7.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varbinary(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'xiaoli','wangke0310'),(2,'wangke1','wangke0310'),(3,'wangke2','wangke0310'),(4,'admin','admin');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add admin',7,'add_admin'),(20,'Can change admin',7,'change_admin'),(21,'Can delete admin',7,'delete_admin'),(22,'Can add auth group',8,'add_authgroup'),(23,'Can change auth group',8,'change_authgroup'),(24,'Can delete auth group',8,'delete_authgroup'),(25,'Can add auth group permissions',9,'add_authgrouppermissions'),(26,'Can change auth group permissions',9,'change_authgrouppermissions'),(27,'Can delete auth group permissions',9,'delete_authgrouppermissions'),(28,'Can add auth permission',10,'add_authpermission'),(29,'Can change auth permission',10,'change_authpermission'),(30,'Can delete auth permission',10,'delete_authpermission'),(31,'Can add auth user',11,'add_authuser'),(32,'Can change auth user',11,'change_authuser'),(33,'Can delete auth user',11,'delete_authuser'),(34,'Can add auth user groups',12,'add_authusergroups'),(35,'Can change auth user groups',12,'change_authusergroups'),(36,'Can delete auth user groups',12,'delete_authusergroups'),(37,'Can add auth user user permissions',13,'add_authuseruserpermissions'),(38,'Can change auth user user permissions',13,'change_authuseruserpermissions'),(39,'Can delete auth user user permissions',13,'delete_authuseruserpermissions'),(40,'Can add classroom',14,'add_classroom'),(41,'Can change classroom',14,'change_classroom'),(42,'Can delete classroom',14,'delete_classroom'),(43,'Can add course',15,'add_course'),(44,'Can change course',15,'change_course'),(45,'Can delete course',15,'delete_course'),(46,'Can add django admin log',16,'add_djangoadminlog'),(47,'Can change django admin log',16,'change_djangoadminlog'),(48,'Can delete django admin log',16,'delete_djangoadminlog'),(49,'Can add django content type',17,'add_djangocontenttype'),(50,'Can change django content type',17,'change_djangocontenttype'),(51,'Can delete django content type',17,'delete_djangocontenttype'),(52,'Can add django migrations',18,'add_djangomigrations'),(53,'Can change django migrations',18,'change_djangomigrations'),(54,'Can delete django migrations',18,'delete_djangomigrations'),(55,'Can add django session',19,'add_djangosession'),(56,'Can change django session',19,'change_djangosession'),(57,'Can delete django session',19,'delete_djangosession'),(58,'Can add school',20,'add_school'),(59,'Can change school',20,'change_school'),(60,'Can delete school',20,'delete_school'),(61,'Can add student',21,'add_student'),(62,'Can change student',21,'change_student'),(63,'Can delete student',21,'delete_student'),(64,'Can add teacher',22,'add_teacher'),(65,'Can change teacher',22,'change_teacher'),(66,'Can delete teacher',22,'delete_teacher');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classroom`
--

DROP TABLE IF EXISTS `classroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classroom` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(54) DEFAULT NULL COMMENT '班级名称',
  `places` int(2) DEFAULT NULL COMMENT '班级可容纳的人数',
  `school_id` int(4) DEFAULT NULL COMMENT '班级所在的校区id',
  `remark` varchar(104) DEFAULT NULL COMMENT '备注',
  `is_delete` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `classroom_school_id_fk` (`school_id`),
  CONSTRAINT `classroom_school_id_fk` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classroom`
--

LOCK TABLES `classroom` WRITE;
/*!40000 ALTER TABLE `classroom` DISABLE KEYS */;
INSERT INTO `classroom` VALUES (1,'一号教室',40,1,'这是一个备注信息',1),(2,'二号教室',45,2,'这是另外的一个备注信息',1),(3,'三号教室',50,1,NULL,1),(4,'四号教师',40,1,'',0),(7,'五号教室',40,3,'这是另一个备注信息',0),(8,'六号教室',40,1,'备注信息',0);
/*!40000 ALTER TABLE `classroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(54) DEFAULT NULL COMMENT '课程名',
  `time` varchar(54) DEFAULT NULL,
  `teacher_id` int(4) DEFAULT NULL COMMENT '教师id',
  `class_id` int(4) DEFAULT NULL COMMENT '班级id',
  `remark` varchar(54) DEFAULT NULL,
  `is_delete` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `course_class_fk` (`class_id`),
  KEY `course_teacher_fk` (`teacher_id`),
  CONSTRAINT `course_class_fk` FOREIGN KEY (`class_id`) REFERENCES `classroom` (`id`),
  CONSTRAINT `course_teacher_fk` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'暂无安排','暂无安排',NULL,NULL,NULL,0),(2,'17年寒假老罗新概念1班','周二17：00 周三17：00',2,2,NULL,1),(3,'2017春季许岑剑桥一班级','周一17：00 周三17：00',1,1,'这是一个备注',0),(4,'2017春季许岑剑桥一班级','周一17：00 周三17：00',1,1,'这是一个备注',0),(5,'2017春季许岑剑桥一班级','周一17：00 周三17：00',1,1,'这是一个备注',0),(6,'2017秋季朱洪伟剑桥','周三1700周日1700',6,2,'',0);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'mingjia_admin','admin'),(8,'mingjia_admin','authgroup'),(9,'mingjia_admin','authgrouppermissions'),(10,'mingjia_admin','authpermission'),(11,'mingjia_admin','authuser'),(12,'mingjia_admin','authusergroups'),(13,'mingjia_admin','authuseruserpermissions'),(14,'mingjia_admin','classroom'),(15,'mingjia_admin','course'),(16,'mingjia_admin','djangoadminlog'),(17,'mingjia_admin','djangocontenttype'),(18,'mingjia_admin','djangomigrations'),(19,'mingjia_admin','djangosession'),(20,'mingjia_admin','school'),(21,'mingjia_admin','student'),(22,'mingjia_admin','teacher'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-10-02 16:17:54.122035'),(2,'auth','0001_initial','2017-10-02 16:17:54.374972'),(3,'admin','0001_initial','2017-10-02 16:17:54.439410'),(4,'admin','0002_logentry_remove_auto_add','2017-10-02 16:17:54.472102'),(5,'contenttypes','0002_remove_content_type_name','2017-10-02 16:17:54.536904'),(6,'auth','0002_alter_permission_name_max_length','2017-10-02 16:17:54.555225'),(7,'auth','0003_alter_user_email_max_length','2017-10-02 16:17:54.586308'),(8,'auth','0004_alter_user_username_opts','2017-10-02 16:17:54.595949'),(9,'auth','0005_alter_user_last_login_null','2017-10-02 16:17:54.615189'),(10,'auth','0006_require_contenttypes_0002','2017-10-02 16:17:54.617144'),(11,'auth','0007_alter_validators_add_error_messages','2017-10-02 16:17:54.633179'),(12,'auth','0008_alter_user_username_max_length','2017-10-02 16:17:54.657208'),(13,'sessions','0001_initial','2017-10-02 16:17:54.682440'),(14,'mingjia_admin','0001_initial','2017-10-04 15:31:35.607731');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `school` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `school_name` varchar(104) DEFAULT '' COMMENT '校区的名字',
  `school_address` varchar(204) COMMENT '校区所在的详细地址的位置',
  `remark` varchar(54) DEFAULT NULL,
  `is_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
INSERT INTO `school` VALUES (1,'汊河校区','扬州市华扬西路汊河镇','这是一个备注信息',1),(2,'文昌阁校区','扬州市文昌阁','增加一个备注',1),(3,'东关街校区','扬州市东关街','继续添加一个备注',1),(4,'汊河校区','扬州汊河镇','备注信息',1),(5,'广陵校区','扬州广陵区','备注',0),(6,'某某小学','地址','备注',0),(7,'特设他','test','te',0),(8,'111','111','11',1),(9,'hdueb','bubhjb','bbhbh',1),(10,'www','ww','ww',1),(11,'21','21','21',1),(12,'21','21','21',1),(13,'21','21','21',1),(14,'111','111','111',1),(15,'21','21','21',1),(16,'334','334','334',0),(17,'334','334','334',0),(18,'335','335','335',1),(19,'335','335','335',1),(20,'21','21','21',1),(21,'22222','222','2222',1),(22,'333','333','333',2);
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(24) DEFAULT NULL,
  `gender` char(2) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `entrance_time` date DEFAULT NULL,
  `school_name` varchar(104) DEFAULT NULL COMMENT '就读小学的名字',
  `class_name` int(11) DEFAULT NULL,
  `grade` varchar(2) DEFAULT NULL COMMENT '所在小学的班级',
  `temp_class` int(11) DEFAULT NULL COMMENT '就读的年级，仅仅作为临时字段存储',
  `course_id` int(4) DEFAULT NULL COMMENT '班次id',
  `register_date` date DEFAULT NULL COMMENT '报名的时间',
  `remark` varchar(50) DEFAULT NULL,
  `is_delete` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `student_course_fk` (`course_id`),
  CONSTRAINT `student_course_fk` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (5,'wangke','男','17714574929','2017-10-04','fengji',1,NULL,1,1,'2017-10-04','哈哈',1),(6,'wangke1','男','17714574929','2017-10-04','fengji1',2,NULL,1,1,'2017-10-07','哈哈嘻嘻',1),(7,'小明','男','17714574929','2017-10-04','weimiao',3,NULL,1,6,'2017-10-25','b备注信息',0),(8,'xiaoming1','男','17714574929','2017-10-04','weimiao1',7,NULL,1,1,'2017-10-25','哈哈哈',0),(9,'xiaoli','男','17714574929','2017-10-04','光明小学',5,NULL,1,1,'2017-10-04','备注信息',0),(10,'li','男','17714574929','2017-10-04','光明小学',6,NULL,1,1,'2017-10-04','备注信息',0),(11,'hua','女','17714572222','2017-10-11','test1小学',1,NULL,1,2,'2017-10-07','额尔敦',0),(12,'朱洪伟','男','13218553160','2017-10-17','沛县实验小学',1,NULL,1,2,'2017-10-13','我是朱洪伟',0),(13,'朱洪伟1','男','13218553160','2017-10-17','沛县实验小学',1,NULL,1,2,'2017-10-07','我是朱洪伟',0),(14,'朱洪伟','男','18751528121','2001-10-06','五段小学',2,NULL,17,1,'2017-10-05','我是朱洪伟',0),(15,'mac','男','17714574929','2017-10-03','沛县实验小学',1,NULL,1,1,'2017-10-06','欣赏欣赏',0),(16,'xiaoming1','男','17714574929','2017-10-04','weimiao1',4,NULL,1,1,'2017-10-07','哈哈哈',0),(17,'xiaoming1','男','17714574929','2017-10-04','weimiao1',4,NULL,1,1,'2017-10-07','哈哈哈',0),(18,'xiaoming1','男','17714574929','2017-10-04','weimiao1',4,NULL,1,1,'2017-10-07','哈哈哈',0),(19,'xiaoming1','男','17714574929','2017-10-04','weimiao1',4,NULL,1,1,'2017-10-07','哈哈哈',0),(20,'hua','女','17714572222','2017-10-11','test1小学',1,NULL,1,1,'2017-10-07','额尔敦',0),(21,'hua','女','17714572222','2017-10-11','test1小学',1,NULL,1,2,'2017-10-07','额尔敦',0),(22,'小明小朋友','男','17714574929','2017-10-25','22',1,NULL,1,1,'2017-10-24','入学时间 2017-10-25',0),(23,'小花','男','17714574929','2017-10-23','22',1,NULL,1,1,'2017-10-24','2017-10-24',0),(24,'小花','男','17714574929','2019-09-01','22',1,NULL,-1,1,'2017-10-24','2019-9-1',0),(25,'小花1','男','17714574929','2014-10-23','22',1,NULL,4,1,'2017-10-24','2014-10-23',0),(26,'小花1','男','17714574929','2014-10-24','22',1,NULL,4,3,'2017-10-24','2014-10-24',0),(27,'小花2','男','17714574929','2014-10-25','22',1,NULL,4,3,'2017-10-24','2014-10-25',0),(28,'王珂','男','17714574929','2015-09-01','22',1,NULL,3,5,'2017-10-24','2015-9-1',0),(29,'王珂','男','17714574929','2017-10-24','22',1,NULL,1,5,'2017-10-24','2020-10-23',0),(30,'wangchao','男','13511756432','2017-09-01','22',5,NULL,1,1,'2017-10-25','',0),(31,'chao','男','13511756545','2020-09-01','22',3,NULL,-2,1,'2017-10-25','',0);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) DEFAULT NULL COMMENT '教师姓名',
  `id_number` varchar(18) DEFAULT NULL COMMENT '身份证号码',
  `phone` varchar(12) DEFAULT NULL COMMENT '联系电话',
  `gender` varchar(2) DEFAULT NULL COMMENT '性别',
  `birthday` date DEFAULT NULL COMMENT '出生日期',
  `edu` varchar(54) DEFAULT NULL COMMENT '文化水品',
  `english_level` varchar(54) DEFAULT NULL COMMENT '英语等级',
  `entry_date` date DEFAULT NULL COMMENT '入职时间',
  `leave_date` date DEFAULT NULL COMMENT '离职时间',
  `remark` varchar(54) DEFAULT NULL,
  `is_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (1,'许岑','320322199703100000','17714574365','男','1994-02-01','研究生','英语专业八级','2017-02-16','2017-10-02',NULL,0),(2,'老罗','320322199703100001','17714574363','男','1970-10-22','高中','高中英语水平','2017-06-14','2017-10-04',NULL,0),(3,'王珂','320322199703106814','17714574929','男','1997-03-10','大专','英语三级','2017-10-08',NULL,'不太合格的英语老师',0),(4,'王珂','320322199703106814','17714574929','男','1997-03-10','大专','英语三级','2017-10-08',NULL,'不太合格的英语老师',0),(5,'王珂','320322199703106814','17714574929','男','1997-03-10','大专','英语三级','2017-10-08',NULL,'不太合格的英语老师',NULL),(6,'朱洪伟','320322199703106814','17714574929','男','1997-03-10','大专','英语三级','2017-10-08',NULL,'这是一个备注信息',0),(7,'小花','320322199703106814','17714574929','女','1997-03-10','硕士','八级','2017-10-08',NULL,'这是一个备注信息',0),(8,'小明','320133199703107815','17714574929','男','1997-03-10','本科','英语四级','2017-10-10',NULL,'我是小明',0),(9,'王珂','320322199703106814','17714574929','男','1997-03-10','本科','英语六级','2017-10-24',NULL,'test',0),(10,'王超','320481198209212831','13511756221','男','1982-09-21','本科','英语四级','2017-10-01',NULL,'',0),(11,'王超','320481198209212831','13511756221','男','1982-09-21','本科','英语四级','2017-10-01',NULL,'',0);
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-25  2:47:49
