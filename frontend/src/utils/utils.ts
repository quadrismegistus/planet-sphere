export function countSubstring(str:string, substring:string) {
  const regex = new RegExp(substring, 'g');
  const matches = str.match(regex);
  return matches ? matches.length : 0;
}