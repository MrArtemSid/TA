{$CODEPAGE UTF8}
const
  arrayLength = 50;
var
  inputArray : array [1..arrayLength] of integer;
  i, j, c : integer;

begin
  randomize;
  writeln ('Исходный массив: ');
  for i := 1 to arrayLength do
  begin
    for j:=1 to arrayLength do
      begin
        while (i < j) do
          begin
            inputArray[i] := random(100);
            write (inputArray[i]:4);
          end;
      end;
  end;
  writeln;
  for c := 1 to arrayLength do
  begin
    c := c mod 2;
  end;
  writeln;
  readln;
end.
