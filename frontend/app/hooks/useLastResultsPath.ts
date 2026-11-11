export function useLastResultsPath() {
    const lastResultsPath = useState<string | null>(
        "last-results-path",
        () => null,
    );

    const rememberResultsPath = (path: string) => {
        lastResultsPath.value = path;
    };

    return { lastResultsPath, rememberResultsPath };
}
