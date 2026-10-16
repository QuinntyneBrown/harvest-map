ALTER TABLE "problems" ADD COLUMN "reach" text DEFAULT '' NOT NULL;--> statement-breakpoint
ALTER TABLE "problems" ADD COLUMN "status" text DEFAULT 'Tracked' NOT NULL;--> statement-breakpoint
ALTER TABLE "sources" ADD COLUMN "verified_at" timestamp with time zone;--> statement-breakpoint
ALTER TABLE "sources" ADD COLUMN "added_at" timestamp with time zone DEFAULT now() NOT NULL;