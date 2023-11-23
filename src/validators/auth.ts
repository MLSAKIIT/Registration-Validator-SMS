import { z } from "zod";

export const registerSchema = z.object({
  email: z.string().email(),
  name: z
    .string()
    .min(3, { message: "Your name should not be that short!" })
    .max(255),
  roll: z
    .string()
    .min(8, {  message: "Roll number should be 8 digits long!" } )
    .max(8)
    .refine((val) => !isNaN(val as unknown as number), {
      message: "Roll number should be numeric",
    }),
  year: z.string().min(1,{message:"Choose your year"}).max(4),
  phone: z
  .string()
    .min(13,{message:"Number should start with +91"})
    .max(13)
    .refine((val) => val.startsWith('+91') && !isNaN(val.slice(3) as unknown as number), {
      message: "Invalid country code",
    }),
});
