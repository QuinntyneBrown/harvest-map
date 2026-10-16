/** Two-letter mark for a name: first letters of the first two words, or the first two letters. */
export function initials(name: string) {
  const words = name.trim().split(/\s+/).filter(Boolean);
  if (words.length === 0) return "";
  const letters = words.length > 1 ? words[0][0] + words[1][0] : words[0].slice(0, 2);
  return letters.toUpperCase();
}

/** "Tue 14 Oct" style day label. */
export function dayLabel(d: Date) {
  return d.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" }).replace(",", "");
}

/** "Today 12:04" for today, otherwise the day label. */
export function whenLabel(d: Date, now = new Date()) {
  const sameDay = d.toDateString() === now.toDateString();
  return sameDay ? `Today ${d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" })}` : dayLabel(d);
}
