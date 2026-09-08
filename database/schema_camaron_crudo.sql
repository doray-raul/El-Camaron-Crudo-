-- Esquema inicial de la aplicación El Camarón Crudo.
-- Este archivo se importa únicamente en una base CamaronCrudo vacía.

CREATE TABLE `core_producto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `disponible` tinyint(1) NOT NULL,
  `creado_en` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `core_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_cliente` varchar(150) NOT NULL,
  `correo` varchar(254) NOT NULL,
  `telefono` varchar(25) NOT NULL,
  `direccion` longtext NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `costo_envio` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `creado_en` datetime(6) NOT NULL,
  `usuario_id` int NULL,
  PRIMARY KEY (`id`),
  KEY `core_pedido_usuario_id_idx` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `core_detallepedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(120) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `cantidad` int unsigned NOT NULL,
  `pedido_id` bigint NOT NULL,
  `producto_id` bigint NULL,
  PRIMARY KEY (`id`),
  KEY `core_detallepedido_pedido_id_idx` (`pedido_id`),
  KEY `core_detallepedido_producto_id_idx` (`producto_id`),
  CONSTRAINT `core_detallepedido_pedido_id_fk` FOREIGN KEY (`pedido_id`) REFERENCES `core_pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `core_detallepedido_producto_id_fk` FOREIGN KEY (`producto_id`) REFERENCES `core_producto` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `core_producto` (`nombre`, `descripcion`, `precio`, `imagen`, `disponible`, `creado_en`) VALUES
('Ceviche de Camarón', 'Fresco y picante, con nuestro toque especial.', 120.00, 'img/Logo.jpeg', 1, NOW(6)),
('Camarones al Ajillo', 'Salteados con ajo y mantequilla, una delicia.', 150.00, 'img/Producto1.jpeg', 1, NOW(6)),
('Producto Fresco', 'Selección de mariscos frescos del día.', 180.00, 'img/Producto2.jpeg', 1, NOW(6));
