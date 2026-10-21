// Create text parameter DataFolder first, with a trailing directory separator.
// Set explicit semantic column types in each table query after this function.
(FileName as text) as table =>
let
    Source = Csv.Document(File.Contents(DataFolder & FileName),
        [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Headers
