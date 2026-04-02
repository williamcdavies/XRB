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

const MAX_UPLOAD_SIZE = 5 * 1024 * 1024 * 1024; // 5 GB

export interface UploadProgress {
    loaded: number;
    total: number;
    percent: number;
}

export async function uploadFile(
    api: ApiFetcher,
    file: File,
    path: string,
    onProgress?: (progress: UploadProgress) => void,
): Promise<void> {
    if (file.size > MAX_UPLOAD_SIZE) {
        throw new Error('File exceeds maximum upload size of 5 GB');
    }

    // Use XMLHttpRequest for progress tracking
    const form = new FormData();
    form.append('file', file);
    form.append('path', path);

    // Ensure token is fresh by triggering the api wrapper's auto-refresh
    await api.fetch('/api/data/browse/', { method: 'HEAD' }).catch(() => null);
    const { useAuth } = await import('@/composables/auth');
    const { getAccessToken } = useAuth();
    const token = getAccessToken();

    return new Promise<void>((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/data/upload/');
        if (token) {
            xhr.setRequestHeader('Authorization', `Bearer ${token}`);
        }

        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable && onProgress) {
                onProgress({
                    loaded: e.loaded,
                    total: e.total,
                    percent: Math.round((e.loaded / e.total) * 100),
                });
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve();
            } else {
                const data = JSON.parse(xhr.responseText || '{}');
                reject(new Error(data.error || `Upload failed ${xhr.status}`));
            }
        });

        xhr.addEventListener('error', () => reject(new Error('Upload failed: network error')));
        xhr.addEventListener('abort', () => reject(new Error('Upload cancelled')));

        xhr.send(form);
    });
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
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}