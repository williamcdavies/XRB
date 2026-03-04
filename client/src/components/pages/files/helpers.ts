import type { BrowseItem } from './FileList.vue';

interface ApiFetcher {
    fetch: (input: RequestInfo, init?: RequestInit) => Promise<Response>;
}

export interface BrowseResult {
    items: BrowseItem[];
    path: string;
    username: string | null;
    exists: boolean;
}

export async function browsePath(
    api: ApiFetcher,
    path: string,
    extractUsername = false,
): Promise<BrowseResult> {
    const url = path
        ? `/api/data/browse/?path=${encodeURIComponent(path)}`
        : '/api/data/browse/';
    const res = await api.fetch(url);
    const data = await res.json();

    // path doesn't exist, so return dummy BrowseResult with exists=false
    if (res.status === 404) {
        return { items: [], path, username: null, exists: false };
    }
    
    if (!res.ok) {
        throw new Error(data.error || `Error ${res.status}`);
    }

    const items: BrowseItem[] = data.items ?? [];
    let username: string | null = null;

    if (extractUsername) {
        const userEntry = items.find(
            (i) => i.type === 'directory' && i.path.startsWith('users/'),
        );
        username = userEntry
            ? userEntry.path.split('/').slice(1, 2)[0] ?? null
            : null;
    }

    return { items, path: data.path ?? path, username, exists: true };
}

export async function downloadFile(
    api: ApiFetcher,
    relativePath: string,
): Promise<void> {
    const url = `/api/data/download/?path=${encodeURIComponent(relativePath)}`;
    const res = await api.fetch(url);
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || `Download failed ${res.status}`);
    }

    const blob = await res.blob();
    const name = relativePath.split('/').pop() ?? 'download';
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
}

export async function deleteItem(
    api: ApiFetcher,
    path: string,
): Promise<boolean> {
    const res = await api.fetch(
        `/api/data/delete/?path=${encodeURIComponent(path)}`,
        { method: 'DELETE' },
    );
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || `Delete failed ${res.status}`);
    }
    return true;
}

export async function uploadFile(
    api: ApiFetcher,
    file: File,
    path: string,
): Promise<void> {
    const form = new FormData();
    form.append('file', file);
    form.append('path', path);
    const res = await api.fetch('/api/data/upload/', {
        method: 'POST',
        body: form,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
        throw new Error(data.error || `Upload failed ${res.status}`);
    }
}

export async function createDirectory(
    api: ApiFetcher,
    parent: string,
    name: string,
): Promise<void> {
    const res = await api.fetch('/api/data/mkdir/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: parent, name }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
        throw new Error(data.error || `Failed ${res.status}`);
    }
}

export function formatSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}