alter table app_info add column `company_id` integer;
alter table app_info add column `category_id` integer;
ALTER TABLE `app_info` ADD CONSTRAINT `company_id_refs_id_8c09f511` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`);
ALTER TABLE `app_info` ADD CONSTRAINT `category_id_refs_id_ded823cc` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`);
