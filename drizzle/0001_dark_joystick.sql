CREATE TABLE "initiatives" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"organization_id" uuid NOT NULL,
	"text" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "notifications" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" text NOT NULL,
	"type" text NOT NULL,
	"title" text NOT NULL,
	"detail" text DEFAULT '' NOT NULL,
	"href" text DEFAULT '/' NOT NULL,
	"read_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "activity_entries" ALTER COLUMN "run_id" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "activity_entries" ALTER COLUMN "finding_id" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "sources" ALTER COLUMN "finding_id" DROP NOT NULL;--> statement-breakpoint
ALTER TABLE "activity_entries" ADD COLUMN "subject_kind" text;--> statement-breakpoint
ALTER TABLE "activity_entries" ADD COLUMN "subject_id" uuid;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "type" text DEFAULT 'Community' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "city" text DEFAULT '' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "country" text DEFAULT '' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "website" text DEFAULT '' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "founded" text DEFAULT '' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "reach" text DEFAULT '' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "tags" text[] DEFAULT ARRAY[]::text[] NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "verification_status" text DEFAULT 'Unverified' NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "mark" text;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "lat" double precision;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "lon" double precision;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "archived_at" timestamp with time zone;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "archived_by" text;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "updated_at" timestamp with time zone DEFAULT now() NOT NULL;--> statement-breakpoint
ALTER TABLE "organizations" ADD COLUMN "updated_by" text;--> statement-breakpoint
ALTER TABLE "sources" ADD COLUMN "subject_kind" text;--> statement-breakpoint
ALTER TABLE "sources" ADD COLUMN "subject_id" uuid;--> statement-breakpoint
ALTER TABLE "initiatives" ADD CONSTRAINT "initiatives_organization_id_organizations_id_fk" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "notifications" ADD CONSTRAINT "notifications_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "organizations" ADD CONSTRAINT "organizations_archived_by_users_id_fk" FOREIGN KEY ("archived_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "organizations" ADD CONSTRAINT "organizations_updated_by_users_id_fk" FOREIGN KEY ("updated_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;